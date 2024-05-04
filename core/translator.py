import os
from deep_translator import GoogleTranslator
import re


def read_readme():
    with open("README.md", "r", encoding="utf-8") as file:
        return file.read()


def update_localizations():
    readme_content = read_readme()
    selected_langs = os.getenv("LANGS")
    no_html_content = re.sub(r"<.*?>", "", readme_content)
    no_links_content = re.sub(r"\[([^]]+)]\(([^)]+)\)", r"\1", no_html_content)

    chunk_size = 5000
    chunks = [no_links_content[i:i+chunk_size]
              for i in range(0, len(no_links_content), chunk_size)]

    languages = [lang.strip() for lang in selected_langs.split(",")]
    files = []

    if not os.path.exists("dist"):
        os.makedirs("dist")

    for lang in languages:
        try:
            translated_chunks = [GoogleTranslator(
                source='auto', target=lang).translate(text=chunk) for chunk in chunks]
            translated_content = " ".join(translated_chunks)

            with open(f"dist/{lang}.md", "w", encoding="utf-8") as file:
                file.write(translated_content)
            print(f"Localization for {lang} updated.")
            files.append(f"dist/{lang}.md")
        except Exception as e:
            print(f"Failed to translate to {lang}: {str(e)}")

    return files


update_localizations()