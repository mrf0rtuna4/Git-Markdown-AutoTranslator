import asyncio
import os

import deep_translator

from app.readme_handler import ReadmeHandler
from app.markdown_processor import MarkdownProcessor
from app.logger import log_info, log_error

ERR_CODE_FAILED_TO_TRANSLATE = -1
ERR_CODE_FAILED_TO_WRITE = -2


class LocalizationManager:
    def __init__(self, langs, readme_path="README.md", dist_dir="dist"):
        self.langs = langs
        self.readme_handler = ReadmeHandler(readme_path)
        self.processor = MarkdownProcessor()
        self.dist_dir = dist_dir

    @staticmethod
    async def translate_chunk(chunk, lang):
        translator = deep_translator.GoogleTranslator(
            source='auto', target=lang)
        retry_attempts = 2
        for attempt in range(retry_attempts):
            try:
                return translator.translate(text=chunk)
            except deep_translator.exceptions.RequestError as e:
                if attempt < retry_attempts - 1:
                    log_error(
                        f"❌ Failed to translate to {lang}, attempt {attempt + 1}: {str(e)}")
                    log_info(f"♻️ Retrying after 3 seconds...")
                    await asyncio.sleep(3)
                else:
                    log_error(
                        f"❌ Totally failed to translate to {lang}: {str(e)}")
                    exit(ERR_CODE_FAILED_TO_TRANSLATE)

    async def update_localizations(self):
        """
        Update the localizations for the specified languages.

        :return: updated files
        """
        with open(self.readme_handler.file_path, "r", encoding="utf-8") as file:
            readme_content = file.read()

        chunks, _ = self.processor.decompile_readme(readme_content)
        languages = [lang.strip() for lang in self.langs.split(",")]
        files = []

        if not os.path.exists(self.dist_dir):
            os.makedirs(self.dist_dir)

        tasks = []
        for lang in languages:
            translated_chunks = []
            for chunk in chunks:
                translated_chunk = await self.translate_chunk(chunk, lang)
                translated_chunks.append(translated_chunk)

            translated_content = self.processor.build_readme(translated_chunks, lang)
            self.processor.post_check_placeholders(translated_content)
            task = self.write_to_file(lang, translated_content)
            tasks.append(task)

        files = await asyncio.gather(*tasks)
        log_info("🎉 All localizations updated.")
        return files

    async def write_to_file(self, lang, content):
        """
        Write the translated content to a file.

        :param lang: Language of the translated content.
        :param content: Translated content.
        :return: Path to the written file.
        """
        try:
            file_path = os.path.join(self.dist_dir, f"{lang}.md")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            return file_path
        except Exception as e:
            log_error(
                f"❌ Failed to write translated content for {lang}: {str(e)}")
            exit(ERR_CODE_FAILED_TO_WRITE)
