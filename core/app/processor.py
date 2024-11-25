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

from .logger import log_info, log_error, log_dbg


class Processor:
    def __init__(self):
        self.placeholder_map = {
            "_BL0CK": [],
            "_L1NK": [],
            "_HTML": [],
            "_MD_WDGT": [],
            "_NON_TRANSLATE": []
        }


    @staticmethod
    def _generate_placeholder(placeholder):
        """
        Generate a unique placeholder string without spaces.
        """
        unique_placeholder = f"{placeholder}_{uuid.uuid4().hex}"
        return unique_placeholder.replace(" ", "")


    def clear_placeholder_map(self):
        self.placeholder_map = {
            "_BL0CK": [],
            "_L1NK": [],
            "_HTML": [],
            "_MD_WDGT": [],
            "_NON_TRANSLATE": []
        }


    def _sanitize_placeholders(self, text, placeholder_map):
        patterns = {
            "_BL0CK": r"```[\s\S]*?```",
            "_MD_WDGT": r"!\[[^]]*]\([^)]+\)",
            "_L1NK": r"\[([^]]+)]\(([^)]+)\)",
            "_HTML": r"<.*?>",
            "_NON_TRANSLATE": r"\[\[.*?\]\]"
        }

        for key, pattern in patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                unique_placeholder = self._generate_placeholder(key)
                placeholder_map[key].append((unique_placeholder, match))
                log_dbg(f"Created placeholder: {unique_placeholder} for tag: {key}")
                if isinstance(match, tuple):
                    match_str = "".join(match)
                else:
                    match_str = match
                text = text.replace(match_str, unique_placeholder, 1)

        return text


    def _restore_placeholders(self, text, placeholder_map):
        for placeholder_type, mappings in placeholder_map.items():
            for unique_placeholder, original in mappings:
                if unique_placeholder not in text:
                    log_dbg(f"⚠ Placeholder {unique_placeholder} not found in text.")

                if isinstance(original, tuple):
                    original_str = "".join(original)
                else:
                    original_str = original

                text = text.replace(unique_placeholder, original_str, 1)
        return text


    def decompile_file(self, content, *, file=None):
        content = self._sanitize_placeholders(content, self.placeholder_map)
        chunk_size = 2048
        chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]
        log_info(f"💠 Decompiled {file} file content into chunks.")
        return chunks, self.placeholder_map


    def build_file(self, translated_chunks, placeholder_map, lang, *, file=None):
        translated_content = "".join(translated_chunks)
        log_info(f"📦 Let's start rebuilding translated content for {lang}_{file}")
        translated_content = self._restore_placeholders(translated_content, placeholder_map)
        return translated_content


    def post_check_placeholders(self, translated_content):
        remaining_placeholders = [ph for mappings in self.placeholder_map.values()
                                  for ph, _ in mappings if ph in translated_content]
        if remaining_placeholders:
            log_error(f"❌ Error: Not all placeholders were replaced. Remaining placeholders: {remaining_placeholders}")
            log_error(f"Translated content after attempting to restore placeholders: {translated_content}")
            raise ValueError("Not all placeholders were replaced.")
