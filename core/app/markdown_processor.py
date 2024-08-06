"""
MIT License

Copyright (c) 2024 Mr_Fortuna

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import re
import uuid

from app.logger import log_info, log_error


class MarkdownProcessor:
    def __init__(self):
        self.placeholder_map = {
            "_BL0CK": [],
            "_L1NK": [],
            "_HTML": []
        }

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
        code_blocks = re.findall(r"```[\s\S]*?```", text)
        for code_block in code_blocks:
            unique_placeholder = self._generate_placeholder("_BL0CK")
            self.placeholder_map["_BL0CK"].append(
                (unique_placeholder, code_block))
            text = text.replace(code_block, unique_placeholder, 1)

        links = re.findall(r"\[([^]]+)]\(([^)]+)\)", text)
        for link in links:
            unique_placeholder = self._generate_placeholder("_L1NK")
            self.placeholder_map["_L1NK"].append(
                (unique_placeholder, link))
            text = text.replace(
                f"[{link[0]}]({link[1]})", unique_placeholder, 1)

        html_tags = re.findall(r"<.*?>", text)
        for html_tag in html_tags:
            unique_placeholder = self._generate_placeholder("_HTML")
            self.placeholder_map["_HTML"].append(
                (unique_placeholder, html_tag))
            text = text.replace(html_tag, unique_placeholder, 1)

        return text

    def _restore_placeholders(self, text):
        """
        Restore placeholders to their original form.
        """
        for placeholder_type, mappings in self.placeholder_map.items():
            for unique_placeholder, original in mappings:
                if placeholder_type == "_L1NK":
                    original = f"[{original[0]}]({original[1]})"
                text = text.replace(unique_placeholder, original, 1)
        return text

    def decompile_readme(self, readme_content):
        """
        Decompile the README content into chunks and extract code blocks, links, and HTML tags.

        :return: Tuple containing the chunks of text and a dictionary with extracted data.
        """
        readme_content = self._sanitize_placeholders(readme_content)

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

        log_info("💠 Decompiled README content into chunks.")

        return chunks, self.placeholder_map

    def build_readme(self, translated_chunks, lang):
        """
        Rebuild the translated chunks into a complete translated README content.

        :param translated_chunks: List of translated text chunks.
        :param lang: Language for build
        :return: Translated README content.
        """
        translated_content = " ".join(translated_chunks)
        log_info(f"📦 Let's start rebuilding translated content for {lang}.md")

        translated_content = self._restore_placeholders(translated_content)
        return translated_content

    def post_check_placeholders(self, translated_content):
        """
        Post-check for any remaining placeholders.

        :param translated_content: Translated README content.
        :return: None
        """
        remaining_placeholders = [ph for mappings in self.placeholder_map.values()
                                  for ph, _ in mappings if ph in translated_content]
        if remaining_placeholders:
            log_error(
                f"❌ Error: Not all placeholders were replaced. Remaining placeholders: {remaining_placeholders}")
            log_error(
                f"Translated content after attempting to restore placeholders: {translated_content}")
            raise ValueError("Not all placeholders were replaced.")
