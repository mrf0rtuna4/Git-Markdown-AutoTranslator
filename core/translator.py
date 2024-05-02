import re
from googletrans import Translator
import time

def read_readme():
    with open("README.md", "r", encoding="utf-8") as file:
        return file.read()

def update_localizations():
    readme_content = read_readme()
    translator = Translator()

    no_links_content = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", readme_content)

    src_lang = None
    while src_lang is None:
        try:
            src_lang = translator.detect(no_links_content).lang
        except AttributeError:
            time.sleep(1)

    languages = ['ru', 'fr', 'es']
    for lang in languages:
        if lang != src_lang:
            translated_content = translator.translate(no_links_content, src=src_lang, dest=lang).text
            with open(f"locales/{lang}.md", "w", encoding="utf-8") as file:
                file.write(translated_content)
            print(f"Localization for {lang} updated.")

update_localizations()
