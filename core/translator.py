import os
import asyncio
from deep_translator import GoogleTranslator
import re


async def decompile_readme():
    """
    Decompile the README file into chunks and extract code blocks, links, and HTML tags.

    :return: Tuple containing the chunks of text and a dictionary with extracted data.
    """
    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.read()

    code_blocks = re.findall(r"```[\s\S]*?```", readme_content)
    supported_content = re.sub(r"```[\s\S]*?```", "10001", readme_content)
    links = re.findall(r"\[([^]]+)]\(([^)]+)\)", supported_content)
    supported_content = re.sub(r"\[([^]]+)]\(([^)]+)\)", "10002", supported_content)
    html_tags = re.findall(r"<.*?>", supported_content)
    supported_content = re.sub(r"<.*?>", "10003", supported_content)

    chunk_size = 5000
    chunks = [supported_content[i:i + chunk_size]
              for i in range(0, len(supported_content), chunk_size)]

    print("💠 Let's start collecting the content.")

    return chunks, {"code_blocks": code_blocks, "links": links, "html_tags": html_tags}


async def build_readme(translated_chunks, data):
    """
    Rebuild the translated chunks into a complete translated README content.

    :param translated_chunks: List of translated text chunks.
    :param data: Dictionary containing extracted data like code blocks, links, and HTML tags.
    :return: Translated README content.
    """
    translated_content = " ".join(translated_chunks)
    print("📦 Let's start building the translation.")

    for i, code_block in enumerate(data["code_blocks"]):
        translated_content = translated_content.replace(f"10001", code_block, 1)

    for i, link in enumerate(data["links"]):
        translated_content = translated_content.replace(f"10002", f"[{link[0]}]({link[1]})", 1)

    for i, html_tag in enumerate(data["html_tags"]):
        translated_content = translated_content.replace(f"10003", html_tag, 1)

    return translated_content


async def update_localizations():
    """
    Update the localizations for the specified languages.

    :return: updated files
    """
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
            print(f"✅ Localization for {lang} updated.")
            files.append(f"dist/{lang}.md")
        except Exception as e:
            print(f"❌ Failed to translate to {lang}: {str(e)}")

    print("🎉 All localizations updated.")
    return files


async def main():
    await update_localizations()


asyncio.run(main())
