import os
import asyncio
from deep_translator import GoogleTranslator
import re


async def decompile_readme():
    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.read()

    code_blocks = re.findall(r"```[\s\S]*?```", readme_content)
    non_code_blocks = re.sub(r"```[\s\S]*?```", "CoDE_Bl0CK", readme_content)
    links = re.findall(r"\[([^]]+)]\(([^)]+)\)", non_code_blocks)
    non_code_blocks = re.sub(r"\[([^]]+)]\(([^)]+)\)", "LIНК", non_code_blocks)
    html_tags = re.findall(r"<.*?>", non_code_blocks)
    non_code_blocks = re.sub(r"<.*?>", "H3ML_TEG", non_code_blocks)

    chunk_size = 5000
    chunks = [non_code_blocks[i:i + chunk_size]
              for i in range(0, len(non_code_blocks), chunk_size)]

    return chunks, {"code_blocks": code_blocks, "links": links, "html_tags": html_tags}


async def build_readme(translated_chunks, data):
    translated_content = " ".join(translated_chunks)

    for i, code_block in enumerate(data["code_blocks"]):
        translated_content = translated_content.replace(f"CoDE_Bl0CK", code_block, 1)

    for i, link in enumerate(data["links"]):
        translated_content = translated_content.replace(f"LIНК", f"[{link[0]}]({link[1]})", 1)

    for i, html_tag in enumerate(data["html_tags"]):
        translated_content = translated_content.replace(f"H3ML_TEG", html_tag, 1)

    return translated_content


async def update_localizations():
    every = await decompile_readme()
    chunks = every[0]
    data = every[1]
    selected_langs = os.getenv("LANGS")

    languages = [lang.strip() for lang in selected_langs.split(",")]
    files = []

    if not os.path.exists("dist"):
        os.makedirs("dist")

    for lang in languages:
        try:
            translated_chunks = []
            for chunk in chunks:
                translated_chunk = GoogleTranslator(source='auto', target=lang).translate(text=chunk)
                translated_chunks.append(translated_chunk)

            translated_content = await build_readme(translated_chunks, data)

            with open(f"dist/{lang}.md", "w", encoding="utf-8") as file:
                file.write(translated_content)
            print(f"Localization for {lang} updated.")
            files.append(f"dist/{lang}.md")
        except Exception as e:
            print(f"Failed to translate to {lang}: {str(e)}")

    return files


async def main():
    await update_localizations()

asyncio.run(main())
