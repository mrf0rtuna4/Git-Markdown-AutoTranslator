import os
import asyncio

import deep_translator
from readme_handler import ReadmeHandler

################################
#     Development Varibles     #
from dotenv import load_dotenv


load_dotenv()
#         DO NOT USE           #
################################


ERR_CODE_FAILED_TO_TRANSLATE = -1
ERR_CODE_FAILED_TO_WRITE = -2


class LocalizationManager:
    def __init__(self, langs, readme_path="README.md", dist_dir="dist"):
        self.langs = langs
        self.readme_handler = ReadmeHandler(readme_path)
        self.dist_dir = dist_dir

    async def update_localizations(self):
        """
        Update the localizations for the specified languages.

        :return: updated files
        """
        chunks, data = await self.readme_handler.decompile_readme()
        languages = [lang.strip() for lang in self.langs.split(",")]
        files = []

        if not os.path.exists(self.dist_dir):
            os.makedirs(self.dist_dir)

        tasks = []
        for lang in languages:
            translated_chunks = []

            for chunk in chunks:
                def translate_chunk():
                    translated_chunk = deep_translator.GoogleTranslator(
                        source='auto', target=lang).translate(text=chunk)
                    translated_chunks.append(translated_chunk)
                try:
                    translate_chunk()
                except deep_translator.exceptions.RequestError as e:
                    print(f"❌ Failed to translate to {lang}: {str(e)}")
                    print(f"♻️ Retrying after 3 seconds...")
                    try:
                        translate_chunk()
                    except deep_translator.exceptions.RequestError as e:
                        print(f"❌ Totally failed to translate to {lang}: {str(e)}")
                        exit(ERR_CODE_FAILED_TO_TRANSLATE)

            task = self.readme_handler.build_readme(
                translated_chunks, data)
            tasks.append(task)

        translated_contents = await asyncio.gather(*tasks)

        for lang, translated_content in zip(languages, translated_contents):
            try:
                file_path = os.path.join(self.dist_dir, f"{lang}.md")
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(translated_content)
                print(f"✅ Localization for {lang} updated.")
                files.append(file_path)
            except Exception as e:
                print(f"❌ Failed to write translated content for {lang}: {str(e)}")
                exit(ERR_CODE_FAILED_TO_WRITE)

        print("🎉 All localizations updated.")
        return files


async def main():
    selected_langs = os.getenv("LANGS")
    if selected_langs is None:
        print("❌ LANGS environment variable not set.")
        return
    manager = LocalizationManager(selected_langs)
    await manager.update_localizations()

asyncio.run(main())
