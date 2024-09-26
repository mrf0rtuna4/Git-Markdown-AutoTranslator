"""
MIT License

Copyright (c) 2024 Mr_Fortuna

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio
import os

from app.logger import log_info, log_error
from app.markdown_processor import MarkdownProcessor
from deep_translator import GoogleTranslator


class LocalizationManager:
    def __init__(self, langs, files, dist_dir="dist"):
        if isinstance(files, str):
            self.files = [file.strip() for file in files.split(",")]
        else:
            self.files = files if isinstance(files, list) else [files]

        self.langs = [lang.strip() for lang in langs.split(",")]
        self.processor = MarkdownProcessor()
        self.dist_dir = dist_dir

    @staticmethod
    async def translate_text(text, lang):
        translator = GoogleTranslator(source='auto', target=lang)
        try:
            return translator.translate(text)
        except Exception as e:
            log_error(f"Translation failed for {lang}: {str(e)}")
            raise

    async def process_file(self, file_path):
        # log_info(f"Processing file: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        chunks, _ = self.processor.decompile_readme(content, file=file_path)
        translations = {lang: [] for lang in self.langs}

        for chunk in chunks:
            translation_tasks = [self.translate_text(chunk, lang) for lang in self.langs]
            translated_chunks = await asyncio.gather(*translation_tasks)
            for lang, translated_chunk in zip(self.langs, translated_chunks):
                translations[lang].append(translated_chunk)

        for lang, translated_chunks in translations.items():
            translated_content = self.processor.build_readme(translated_chunks, lang)
            self.processor.post_check_placeholders(translated_content)
            await self.write_to_file(file_path, lang, translated_content)

    async def write_to_file(self, original_file, lang, content):
        base_name = os.path.basename(original_file)
        file_path = os.path.join(self.dist_dir, f"{lang}_{base_name}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            log_info(f"⌛ File saved: {file_path}")
        except Exception as e:
            log_error(f"Failed to write file for {lang}: {str(e)}")
            raise

    async def update_localizations(self):
        tasks = [self.process_file(file_path) for file_path in self.files]
        await asyncio.gather(*tasks)
        log_info("🎈 All files have been processed.")
