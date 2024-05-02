import re
from googletrans import Translator
import time

def read_readme():
    with open("README.md", "r", encoding="utf-8") as file:
        return file.read()

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

    src_lang = translator.detect(no_links_content).lang

    languages = ['ru', 'fr', 'es']
    for lang in languages:
        if lang != src_lang:
            chunk_size = 5000
            chunks = [no_links_content[i:i+chunk_size] for i in range(0, len(no_links_content), chunk_size)]
            translated_chunks = [translator.translate(chunk, src=src_lang, dest=lang).text for chunk in chunks]
            translated_content = ''.join(translated_chunks)

            with open(f"{lang}.md", "w", encoding="utf-8") as file:
                file.write(translated_content)
            print(f"Localization for {lang} updated.")


update_localizations()
