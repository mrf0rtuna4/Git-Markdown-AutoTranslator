"""
MIT License

Copyright (c) 2024-2026 Mr_Fortuna

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
from dataclasses import dataclass

from .logger import log_dbg, log_error, log_info

EXCLUDED_ADMONITIONS = ("IMPORTANT", "CAUTION", "TIP", "WARNING")
PROTECTED_PLACEHOLDER = "_MD_PROTECTED"


@dataclass(frozen=True)
class MarkdownRange:
    start: int
    end: int
    kind: str


class Processor:
    def __init__(self):
        self.placeholder_map = {
            key: []
            for key in (
                "_BL0CK",
                "_L1NK",
                "_HTML",
                "_MD_WDGT",
                "_NON_TRANSLATE",
                "_MD_BLOCK_NOTE",
                PROTECTED_PLACEHOLDER,
            )
        }
        self._markdown = self._build_markdown_parser()

    @staticmethod
    def _build_markdown_parser():
        try:
            from markdown_it import MarkdownIt
        except ImportError:
            log_dbg(
                "markdown-it-py is unavailable; using conservative fallback parser")
            return None

        parser = MarkdownIt("commonmark", {"html": True})
        for rule in ("table", "strikethrough"):
            try:
                parser.enable(rule)
            except ValueError:
                log_dbg(f"markdown-it-py rule is unavailable: {rule}")
        return parser

    @staticmethod
    def _generate_placeholder(prefix):
        return f"{prefix}_{uuid.uuid4().hex}"

    def clear_placeholder_map(self):
        self.placeholder_map = {k: [] for k in self.placeholder_map}

    def _store_placeholder(self, key, original, placeholder_map):
        unique_placeholder = self._generate_placeholder(key)
        placeholder_map.setdefault(key, []).append(
            (unique_placeholder, original))
        log_dbg(f"Created placeholder: {unique_placeholder} for tag: {key}")
        return unique_placeholder

    @staticmethod
    def _merge_ranges(ranges):
        merged = []
        for current in sorted(ranges, key=lambda item: (item.start, item.end)):
            if current.start >= current.end:
                continue
            if not merged or current.start > merged[-1].end:
                merged.append(current)
                continue
            previous = merged[-1]
            merged[-1] = MarkdownRange(
                previous.start,
                max(previous.end, current.end),
                f"{previous.kind},{current.kind}",
            )
        return merged

    @staticmethod
    def _frontmatter_range(lines):
        if not lines or lines[0].strip() not in {"---", "+++"}:
            return None

        marker = lines[0].strip()
        for index in range(1, len(lines)):
            if lines[index].strip() == marker:
                return MarkdownRange(0, index + 1, "frontmatter")
        return None

    @staticmethod
    def _line_starts_mdx_statement(line):
        stripped = line.strip()
        return bool(
            re.match(r"^(import|export)\s+", stripped)
            or re.match(r"^<[A-Z][\w.:]*(\s|>|/>)", stripped)
            or re.match(r"^</[A-Z][\w.:]*\s*>", stripped)
        )
    
    @staticmethod
    def asd():
        a = 1
        return bool(a)

    @staticmethod
    def _admonition_type(line):
        match = re.match(r"^\s*>\s*\[!([A-Z]+)]", line)
        return match.group(1) if match else None

    def _fallback_ranges(self, lines):
        protected = []
        translatable = []
        index = 0

        frontmatter = self._frontmatter_range(lines)
        if frontmatter:
            protected.append(frontmatter)
            index = frontmatter.end

        while index < len(lines):
            line = lines[index]
            stripped = line.strip()

            if not stripped:
                index += 1
                continue

            if re.match(r"^(```|~~~)", stripped):
                marker = stripped[:3]
                start = index
                index += 1
                while index < len(lines) and not lines[index].strip().startswith(
                    marker
                ):
                    index += 1
                index = min(index + 1, len(lines))
                protected.append(MarkdownRange(start, index, "fence"))
                continue

            admonition = self._admonition_type(line)
            if admonition in EXCLUDED_ADMONITIONS:
                start = index
                index += 1
                while index < len(lines) and lines[index].strip().startswith(">"):
                    index += 1
                protected.append(MarkdownRange(start, index, "admonition"))
                continue

            if stripped.startswith("|") and "|" in stripped[1:]:
                start = index
                while index < len(lines) and lines[index].strip().startswith("|"):
                    index += 1
                protected.append(MarkdownRange(start, index, "table"))
                continue

            if stripped.startswith("<") and stripped.endswith(">"):
                start = index
                index += 1
                while index < len(lines) and lines[index].strip():
                    if lines[index].strip().startswith("</"):
                        index += 1
                        break
                    if not lines[index].startswith((" ", "\t", "<")):
                        break
                    index += 1
                protected.append(MarkdownRange(start, index, "html"))
                continue

            if self._line_starts_mdx_statement(line):
                protected.append(MarkdownRange(index, index + 1, "mdx"))
                index += 1
                continue

            start = index
            index += 1
            while index < len(lines) and lines[index].strip():
                next_line = lines[index]
                if (
                    re.match(r"^(```|~~~)", next_line.strip())
                    or self._admonition_type(next_line) in EXCLUDED_ADMONITIONS
                    or next_line.strip().startswith("|")
                    or self._line_starts_mdx_statement(next_line)
                ):
                    break
                index += 1
            translatable.append(MarkdownRange(start, index, "text"))

        return protected, translatable

    def _markdown_it_ranges(self, text, lines):
        if self._markdown is None:
            return self._fallback_ranges(lines)

        protected = []
        translatable = []
        tokens = self._markdown.parse(text)

        frontmatter = self._frontmatter_range(lines)
        if frontmatter:
            protected.append(frontmatter)

        blockquote_stack = []
        for token in tokens:
            token_map = token.map
            if token.type in {"fence", "code_block", "html_block"} and token_map:
                protected.append(MarkdownRange(
                    token_map[0], token_map[1], token.type))

            if token.type == "table_open" and token_map:
                protected.append(MarkdownRange(
                    token_map[0], token_map[1], "table"))

            if token.type == "blockquote_open" and token_map:
                blockquote_stack.append(token_map)
            elif token.type == "blockquote_close" and blockquote_stack:
                blockquote_map = blockquote_stack.pop()
                first_line = (
                    lines[blockquote_map[0]] if blockquote_map[0] < len(
                        lines) else ""
                )
                if self._admonition_type(first_line) in EXCLUDED_ADMONITIONS:
                    protected.append(
                        MarkdownRange(
                            blockquote_map[0], blockquote_map[1], "admonition"
                        )
                    )

            if (
                token.type in {"paragraph_open",
                               "heading_open", "list_item_open"}
                and token_map
            ):
                translatable.append(
                    MarkdownRange(token_map[0], token_map[1], token.type)
                )

        for index, line in enumerate(lines):
            if self._line_starts_mdx_statement(line):
                protected.append(MarkdownRange(index, index + 1, "mdx"))

        return self._merge_ranges(protected), self._merge_ranges(translatable)

    @staticmethod
    def _range_starts(ranges, index):
        for current in ranges:
            if current.start == index:
                return current
        return None

    @staticmethod
    def _is_within_ranges(ranges, index):
        return any(current.start <= index < current.end for current in ranges)

    def _split_translation_unit(self, unit, max_line_length):
        if len(unit) <= max_line_length:
            return [unit]

        parts = []
        current = []
        current_len = 0
        for line in unit.splitlines():
            projected = current_len + len(line) + (1 if current else 0)
            if current and projected > max_line_length:
                parts.append("\n".join(current))
                current = [line]
                current_len = len(line)
            else:
                current.append(line)
                current_len = projected

        if current:
            parts.append("\n".join(current))
        return parts

    def _decompile_with_ast(self, content, placeholder_map, max_line_length):
        lines = content.splitlines()
        protected_ranges, translatable_ranges = self._markdown_it_ranges(
            content, lines)
        protected_ranges = self._merge_ranges(protected_ranges)
        translatable_ranges = self._merge_ranges(
            range_item
            for range_item in translatable_ranges
            if not any(
                protected.start < range_item.end and range_item.start < protected.end
                for protected in protected_ranges
            )
        )

        output = []
        index = 0
        while index < len(lines):
            protected = self._range_starts(protected_ranges, index)
            if protected:
                original = "\n".join(lines[protected.start: protected.end])
                key = (
                    "_MD_BLOCK_NOTE"
                    if "admonition" in protected.kind
                    else PROTECTED_PLACEHOLDER
                )
                output.append(self._store_placeholder(
                    key, original, placeholder_map))
                index = protected.end
                continue
            translatable = self._range_starts(translatable_ranges, index)
            if translatable:
                original = "\n".join(
                    lines[translatable.start: translatable.end])
                output.extend(self._split_translation_unit(
                    original, max_line_length))
                index = translatable.end
                continue

            if self._is_within_ranges(
                protected_ranges, index
            ) or self._is_within_ranges(translatable_ranges, index):
                index += 1
                continue

            output.append(lines[index] if lines[index].strip() else "")
            index += 1

        return output

    @staticmethod
    def _restore_placeholders(text, placeholder_map):
        for mappings in placeholder_map.values():
            for ph, original in mappings:
                text = text.replace(ph, original)
        return text

    def decompile_file(self, content, *, file=None, max_line_length=500):
        self.clear_placeholder_map()
        lines = self._decompile_with_ast(
            content, self.placeholder_map, max_line_length)
        log_info(
            f"💠 Decompiled {file} into {len(lines)} AST translation units.")
        return lines, self.placeholder_map

    def build_file(self, translated_lines, placeholder_map, lang, *, file=None):
        content = "\n".join(
            line if line is not None else "" for line in translated_lines
        )
        log_info(f"📦 Rebuilding {lang}_{file}")
        text = self._restore_placeholders(content, placeholder_map)
        text = re.sub(r"(\*\*|__)[ \t]*(.*?)[ \t]*(\1)", r"\1\2\1", text)
        return text

    def post_check_placeholders(self, translated_content):
        rem = [
            ph
            for maps in self.placeholder_map.values()
            for ph, _ in maps
            if ph in translated_content
        ]
        if rem:
            log_error(f"❌ Placeholders left: {rem}")
            raise ValueError("Unreplaced placeholders")
