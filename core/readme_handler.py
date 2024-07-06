import re
import uuid


class ReadmeHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def _generate_placeholder(placeholder):
        """
        Generate a unique placeholder string.
        """
        return f"{placeholder}_{uuid.uuid4().hex}"

    def _sanitize_placeholders(self, text):
        """
        Ensure placeholders don't conflict with the original content.
        """
        placeholder_map = {
            "ENCODED_BLOCK": [],
            "ENCODED_LINK": [],
            "ENCODED_HTML": []
        }

        code_blocks = re.findall(r"```[\s\S]*?```", text)
        for code_block in code_blocks:
            unique_placeholder = self._generate_placeholder("ENCODED_BLOCK")
            placeholder_map["ENCODED_BLOCK"].append(
                (unique_placeholder, code_block))
            text = text.replace(code_block, unique_placeholder, 1)

        links = re.findall(r"\[([^]]+)]\(([^)]+)\)", text)
        for link in links:
            unique_placeholder = self._generate_placeholder("ENCODED_LINK")
            placeholder_map["ENCODED_LINK"].append((unique_placeholder, link))
            text = text.replace(
                f"[{link[0]}]({link[1]})", unique_placeholder, 1)

        html_tags = re.findall(r"<.*?>", text)
        for html_tag in html_tags:
            unique_placeholder = self._generate_placeholder("ENCODED_HTML")
            placeholder_map["ENCODED_HTML"].append(
                (unique_placeholder, html_tag))
            text = text.replace(html_tag, unique_placeholder, 1)

        return text, placeholder_map

    @staticmethod
    def _restore_placeholders(text, placeholder_map):
        """
        Restore placeholders to their original form.
        """
        for placeholder_type, mappings in placeholder_map.items():
            for unique_placeholder, original in mappings:
                if placeholder_type == "ENCODED_LINK":
                    original = f"[{original[0]}]({original[1]})"
                text = text.replace(unique_placeholder, original, 1)
        return text

    async def decompile_readme(self):
        """
        Decompile the README file into chunks and extract code blocks, links, and HTML tags.

        :return: Tuple containing the chunks of text and a dictionary with extracted data.
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            readme_content = file.read()

        readme_content, placeholder_map = self._sanitize_placeholders(
            readme_content)

        chunk_size = 2048
        chunks = []
        i = 0

        while i < len(readme_content):
            end_index = min(i + chunk_size, len(readme_content))
            if end_index < len(readme_content):
                while end_index > i and not readme_content[end_index].isspace():
                    end_index -= 1
            chunks.append(readme_content[i:end_index])
            i = end_index

        print("💠 Let's start collecting the content.")
        print(f"Decompiled content: {chunks}")

        return chunks, placeholder_map

    async def build_readme(self, translated_chunks, placeholder_map):
        """
        Rebuild the translated chunks into a complete translated README content.

        :param translated_chunks: List of translated text chunks.
        :param placeholder_map: Dictionary containing extracted data like code blocks, links, and HTML tags.
        :return: Translated README content.
        """
        translated_content = " ".join(translated_chunks)
        print("📦 Let's start building the translation.")

        translated_content = self._restore_placeholders(
            translated_content, placeholder_map)

        # Post-check for any remaining placeholders
        remaining_placeholders = [ph for mappings in placeholder_map.values(
        ) for ph, _ in mappings if ph in translated_content]
        if remaining_placeholders:
            print(
                f"❌ Error: Not all placeholders were replaced. Remaining placeholders: {remaining_placeholders}")
            print(
                f"Translated content after attempting to restore placeholders: {translated_content}")
            raise ValueError("Not all placeholders were replaced.")

        return translated_content
