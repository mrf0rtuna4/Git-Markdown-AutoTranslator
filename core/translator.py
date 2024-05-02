from deep_translator import GoogleTranslator
import re
import os


def read_readme():
    with open("README.md", "r", encoding="utf-8") as file:
        return file.read()


def update_localizations():
    langs = GoogleTranslator().get_supported_languages()
    readme_content = read_readme()
    selected_langs = os.getenv("LANGS")

    no_links_content = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", readme_content)

    languages = [lang.strip() for lang in selected_langs.split(",")]
    for lang in languages:
        try:
            translated_content = GoogleTranslator(
                source='auto', target=lang).translate(text=no_links_content)

            with open(f"{lang}.md", "w", encoding="utf-8") as file:
                file.write(translated_content)
            print(f"Localization for {lang} updated.")
        except Exception as e:
            print(f"Failed to translate to {lang}: {str(e)}")



update_localizations()
