"""
MIT License

Copyright (c) 2024-2025 Mr_Fortuna

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
        self.placeholder_map = {key: [] for key in (
            '_BL0CK', '_L1NK', '_HTML', '_MD_WDGT', '_NON_TRANSLATE')}

    @staticmethod
    def _generate_placeholder(prefix):
        return f"{prefix}_{uuid.uuid4().hex}"

    def clear_placeholder_map(self):
        self.placeholder_map = {k: [] for k in self.placeholder_map}

    def _sanitize_placeholders(self, text, placeholder_map):
        patterns = {
            "_BL0CK": r"```[\s\S]*?```",
            "_MD_WDGT": r"!\[[^]]*]\([^)]+\)",
            "_L1NK": r"\[([^]]+)]\(([^)]+)\)",
            "_HTML": r"<.*?>",
            "_NON_TRANSLATE": r"\[\[.*?\]\]"
        }

        lines = text.splitlines()
        processed_lines = []
        for line in lines:
            if line.strip().startswith("> [!"):
                unique_placeholder = self._generate_placeholder("_MD_BLOCK_NOTE")
                placeholder_map.setdefault("_MD_BLOCK_NOTE", []).append((unique_placeholder, line))
                log_dbg(f"Created block-note placeholder: {unique_placeholder} for line: {line}")
                processed_lines.append(unique_placeholder)
            else:
                processed_lines.append(line)

        text = "\n".join(processed_lines)

        for key, pattern in patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                unique_placeholder = self._generate_placeholder(key)
                match_str = "".join(match) if isinstance(match, tuple) else match
                placeholder_map[key].append((unique_placeholder, match_str))
                log_dbg(f"Created placeholder: {unique_placeholder} for tag: {key}")
                text = text.replace(match_str, unique_placeholder, 1)
        return text

    @staticmethod
    def _restore_placeholders(text, placeholder_map):
        for key, mappings in placeholder_map.items():
            for ph, original in mappings:
                text = text.replace(ph, original)
        return text

    def decompile_file(self, content, *, file=None, max_line_length=500):
        self.clear_placeholder_map()
        text = self._sanitize_placeholders(content, self.placeholder_map)
        lines = []
        for raw in text.splitlines():
            if not raw.strip():
                lines.append('')
                continue
            line = raw
            while len(line) > max_line_length:
                idx = line[:max_line_length].rfind(' ') or max_line_length
                lines.append(line[:idx])
                line = line[idx:].lstrip()
            lines.append(line)
        log_info(f"💠 Decompiled {file} into {len(lines)} lines.")
        return lines, self.placeholder_map

    def build_file(self, translated_lines, placeholder_map, lang, *, file=None):
        content = '\n'.join(line if line is not None else '' for line in translated_lines)
        log_info(f"📦 Rebuilding {lang}_{file}")
        text = self._restore_placeholders(content, placeholder_map)
        text = re.sub(r"(\*\*|__)[ \t]*(.*?)[ \t]*(\1)", r"\1\2\1", text)
        return text

    def post_check_placeholders(self, translated_content):
        rem = [ph for maps in self.placeholder_map.values()
               for ph, _ in maps if ph in translated_content]
        if rem:
            log_error(f"❌ Placeholders left: {rem}")
            raise ValueError("Unreplaced placeholders")
