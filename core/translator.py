from deep_translator import GoogleTranslator
import re


def read_readme():
    with open("README.md", "r", encoding="utf-8") as file:
        return file.read()

def update_localizations():
    readme_content = read_readme()
    no_links_content = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", readme_content)
    src_lang = GoogleTranslator().detect(text=no_links_content)
    languages = ['ru', 'fr', 'es']

    for lang in languages:
        if lang != src_lang:
            translated_content = GoogleTranslator(source='auto', target=lang).translate(text=no_links_content)

            with open(f"{lang}.md", "w", encoding="utf-8") as file:
                file.write(translated_content)
            print(f"Localization for {lang} updated.")

update_localizations()