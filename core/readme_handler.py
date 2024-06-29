import re


class ReadmeHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def decompile_readme(self):
        """
        Decompile the README file into chunks and extract code blocks, links, and HTML tags.

        :return: Tuple containing the chunks of text and a dictionary with extracted data.
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            readme_content = file.read()

        code_blocks = re.findall(r"```[\s\S]*?```", readme_content)
        supported_content = re.sub(
            r"```[\s\S]*?```", "ENCODED_BLOCK", readme_content)
        links = re.findall(r"\[([^]]+)]\(([^)]+)\)", supported_content)
        supported_content = re.sub(
            r"\[([^]]+)]\(([^)]+)\)", "ENCODED_LINK", supported_content)
        html_tags = re.findall(r"<.*?>", supported_content)
        supported_content = re.sub(r"<.*?>", "ENCODED_HTML", supported_content)

        chunk_size = 5000
        chunks = [supported_content[i:i + chunk_size]
                  for i in range(0, len(supported_content), chunk_size)]

        print("💠 Let's start collecting the content.")

        return chunks, {"code_blocks": code_blocks, "links": links, "html_tags": html_tags}

    def build_readme(self, translated_chunks, data):
        """
        Rebuild the translated chunks into a complete translated README content.

        :param translated_chunks: List of translated text chunks.
        :param data: Dictionary containing extracted data like code blocks, links, and HTML tags.
        :return: Translated README content.
        """
        translated_content = " ".join(translated_chunks)
        print("📦 Let's start building the translation.")

        for i, code_block in enumerate(data["code_blocks"]):
            translated_content = translated_content.replace(
                f"ENCODED_BLOCK", code_block, 1)

        for i, link in enumerate(data["links"]):
            translated_content = translated_content.replace(
                f"ENCODED_LINK", f"[{link[0]}]({link[1]})", 1)

        for i, html_tag in enumerate(data["html_tags"]):
            translated_content = translated_content.replace(
                f"ENCODED_HTML", html_tag, 1)

        return translated_content
