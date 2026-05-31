#  MIT License
#
#  Copyright (c) 2024-2026. Mr_Fortuna
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
from __future__ import annotations

import asyncio
import os
import re
from re import Pattern
from concurrent.futures import ThreadPoolExecutor

from deep_translator import GoogleTranslator # pyright: ignore[reportMissingTypeStubs]

from .exceptions import FileWriteError, TranslationFailedError
from .logger import Logger
from .processor import Processor


class LocalizationManager:
    def __init__(
        self,
        files: str,
        langs: str,
        max_threads: int = 5,
        max_line_length: int = 500,
        dist_dir: str = "dist",
    ):
        self.files: list[str] = ([file.strip() for file in files.split(",")])
        self.langs: list[str] = [lang.strip() for lang in langs.split(",")]
        self.max_line_length = max_line_length
        self.max_threads = max_threads
        self.semaphore: asyncio.Semaphore = asyncio.Semaphore(max_threads)
        self.translation_executor: ThreadPoolExecutor = ThreadPoolExecutor(
            max_workers=max_threads)
        self.processor: Processor = Processor()
        self.dist_dir = dist_dir
        self._translation_cache: dict[tuple[str, str], str] = {}
        self.logger: Logger = Logger()

    @staticmethod
    def _translate_sync(text: str, lang: str) -> str:
        translator = GoogleTranslator(source="auto", target=lang)

        return translator.translate(text) # pyright: ignore[reportUnknownMemberType]

    async def _run_blocking_translation(self, text: str, lang: str) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.translation_executor, self._translate_sync, text, lang
        )

    def _placeholder_pattern(self) -> Pattern[str] | None:
        placeholders = [
            re.escape(placeholder)
            for placeholders in self.processor.placeholder_map.values()
            for placeholder, _ in placeholders
        ]
        if not placeholders:
            return None
        return re.compile(f"({'|'.join(placeholders)})")

    async def translate_markdown_unit(self, text: str, lang: str) -> str:
        pattern = self._placeholder_pattern()
        if pattern is None or not pattern.search(text):
            return await self.translate_text(text, lang)

        translated_parts: list[str] = []
        for part in pattern.split(text):
            if not part:
                continue
            if pattern.fullmatch(part):
                translated_parts.append(part)
            elif re.search(r"\w", part):
                translated_parts.append(await self.translate_text(part, lang))
            else:
                translated_parts.append(part)
        return "".join(translated_parts)

    async def translate_text(self, text: str, lang: str) -> str:
        cache_key = (lang, text)
        cached = self._translation_cache.get(cache_key)
        if cached is not None:
            return cached

        async with self.semaphore:
            try:
                translated = await self._run_blocking_translation(text, lang)
                self._translation_cache[cache_key] = translated
                return translated
            except Exception as e:
                self.logger.log_error(
                    f"Translation failed for {lang}: {str(e)}")
                raise TranslationFailedError(
                    f"Translation failed for '{lang}'") from e

    async def process_file(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        lines, placeholder_map = self.processor.decompile_file(
            content, file=file_path, max_line_length=self.max_line_length
        )
        translations: dict[str, list[str]] = {lang: [] for lang in self.langs}

        for line in lines:
            if not line.strip():
                for lang in self.langs:
                    translations[lang].append("")
                continue

            placeholder_pattern = self._placeholder_pattern()
            is_placeholder_only = bool(
                placeholder_pattern and placeholder_pattern.fullmatch(
                    line.strip())
            )

            if is_placeholder_only:
                for lang in self.langs:
                    translations[lang].append(line)
                continue

            translation_tasks = [
                self.translate_markdown_unit(line, lang) for lang in self.langs
            ]
            translated_lines = await asyncio.gather(*translation_tasks)
            for lang, translated_line in zip(self.langs, translated_lines):
                translations[lang].append(translated_line)

        for lang, translated_lines in translations.items():
            translated_content = self.processor.build_file(
                translated_lines, placeholder_map, lang, file=file_path
            )
            self.processor.post_check_placeholders(translated_content)
            await self.write_to_file(file_path, lang, translated_content)

    async def write_to_file(
        self,
        original_file: str,
        lang: str,
        content: str,
    ) -> None:
        base_name = os.path.basename(original_file)
        file_path = os.path.join(self.dist_dir, f"{lang}_{base_name}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            self.logger.log_info(f"⌛ File saved: {file_path}")
        except Exception as e:
            self.logger.log_error(
                f"💥 Failed to write file for {lang} ({file_path}): {str(e)}")
            raise FileWriteError(
                f"Failed to write translation file: {file_path}"
            ) from e

    def shutdown(self) -> None:
        self.translation_executor.shutdown(wait=True)

    async def update_localizations(self) -> None:
        try:
            tasks = [self.process_file(file_path) for file_path in self.files]
            await asyncio.gather(*tasks)
            self.logger.log_info("🎈 All files have been processed.")
        finally:
            self.shutdown()
