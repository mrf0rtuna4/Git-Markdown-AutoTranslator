from __future__ import annotations

import asyncio
import os
import re
import time
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from re import Pattern

from deep_translator.exceptions import TooManyRequests

from .exceptions import FileWriteError, TranslationFailedError
from .logger import Logger
from .processor import Processor
from .providers import TranslationProviderFactory


class LocalizationManager:
    def __init__(
        self,
        files: str | Sequence[str],
        langs: str | Sequence[str],
        max_threads: int = 5,
        max_line_length: int = 500,
        dist_dir: str = "dist",
        provider: str = "GoogleTranslator",
        source_language: str = "auto",
        provider_options: str = "",
        max_retries: int = 5,
    ):
        self.files = self._split_csv(files)
        self.langs = self._split_csv(langs)
        self.max_line_length = max_line_length
        self.max_threads = max_threads
        self.max_retries = max_retries
        self.semaphore: asyncio.Semaphore = asyncio.Semaphore(max_threads)
        self.translation_executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=max_threads)
        self.processor: Processor = Processor()
        self.dist_dir = dist_dir
        self.provider = TranslationProviderFactory.canonical_name(provider)
        self.source_language = source_language
        self.provider_options = provider_options
        self._translation_cache: dict[tuple[str, str], str] = {}
        self.logger: Logger = Logger()

    @staticmethod
    def _split_csv(value: str | Sequence[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return [item.strip() for item in value if item.strip()]

    def _translate_sync(self, text: str, lang: str) -> str:
        translator = TranslationProviderFactory.build(
            provider=self.provider,
            source=self.source_language,
            target=lang,
            provider_options=self.provider_options,
        )

        last_exception: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                result = translator.translate(text)

                if result is None:
                    raise TranslationFailedError(
                        f"Provider returned None for '{text[:100]}' -> '{lang}'"
                    )

                return str(result)

            except TooManyRequests as e:
                last_exception = e
                if attempt == self.max_retries:
                    self.logger.log_error(
                        f"Rate limited by provider for '{lang}' after {self.max_retries} attempts"
                    )
                    raise TranslationFailedError(f"Translation failed for '{lang}'") from e

                delay = 1.0 * (2 ** (attempt - 1))
                self.logger.log_warn(
                    f"Rate limited by provider for '{lang}', retrying in {delay:.1f}s "
                    f"(attempt {attempt}/{self.max_retries})"
                )
                time.sleep(delay)

            except Exception as e:
                last_exception = e
                raise TranslationFailedError(f"Translation failed for '{lang}'") from e

        raise TranslationFailedError(f"Translation failed for '{lang}'") from last_exception

    async def validate_provider(self) -> None:
        self.logger.log_info(f"🔎 Validating {self.provider} provider with target {self.langs[0]}")
        await self.translate_text("Hello", self.langs[0])
        self.logger.log_info(f"✅ {self.provider} provider validation succeeded")

    async def _run_blocking_translation(self, text: str, lang: str) -> str | None:
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

    async def translate_markdown_unit(self, text: str, lang: str) -> str | None:
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

                if translated is None:
                    raise TranslationFailedError(f"Empty translation result for '{text[:100]}'")

                translated = str(translated)

                self._translation_cache[cache_key] = translated
                return translated

            except TranslationFailedError:
                raise
            except Exception as e:
                self.logger.log_error(f"Translation failed for {lang}: {e!s}")
                raise TranslationFailedError(f"Translation failed for '{lang}'") from e

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
                placeholder_pattern and placeholder_pattern.fullmatch(line.strip())
            )

            if is_placeholder_only:
                for lang in self.langs:
                    translations[lang].append(line)
                continue

            translation_tasks = [self.translate_markdown_unit(line, lang) for lang in self.langs]
            translated_lines = await asyncio.gather(*translation_tasks)
            for lang, translated_line in zip(self.langs, translated_lines):
                if translated_line is None:
                    self.logger.log_error(f"NULL translation: lang={lang}, line={line!r}")
                    continue
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
            self.logger.log_error(f"💥 Failed to write file for {lang} ({file_path}): {e!s}")
            raise FileWriteError(f"Failed to write translation file: {file_path}") from e

    def shutdown(self) -> None:
        self.translation_executor.shutdown(wait=True)

    async def update_localizations(self) -> None:
        try:
            tasks = [self.process_file(file_path) for file_path in self.files]
            await asyncio.gather(*tasks)
            self.logger.log_info("🎈 All files have been processed.")
        finally:
            self.shutdown()
