import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.app.processor import Processor


class ProcessorAstTests(unittest.TestCase):
    def test_preserves_fenced_code_as_single_placeholder(self):
        content = "# Title\n\n```python\nfor line in lines:\n    print(line)\n```\n\nParagraph text."
        processor = Processor()

        units, placeholder_map = processor.decompile_file(content, file="README.md")

        self.assertIn("# Title", units)
        self.assertIn("Paragraph text.", units)
        self.assertEqual(len(placeholder_map["_MD_PROTECTED"]), 1)
        placeholder, original = placeholder_map["_MD_PROTECTED"][0]
        self.assertIn(placeholder, units)
        self.assertEqual(
            original, "```python\nfor line in lines:\n    print(line)\n```"
        )

        rebuilt = processor.build_file(units, placeholder_map, "es", file="README.md")
        self.assertEqual(rebuilt, content)

    def test_preserves_frontmatter_tables_html_mdx_and_selected_admonitions(self):
        content = "\n".join(
            [
                "---",
                "title: Docs",
                "---",
                "",
                "import Chart from './Chart'",
                "",
                "| Name | Value |",
                "| --- | --- |",
                "| A | B |",
                "",
                "> [!IMPORTANT]",
                "> Keep this exact.",
                "",
                "<div>",
                "  <span>Raw HTML</span>",
                "</div>",
                "",
                "Regular paragraph",
            ]
        )
        processor = Processor()

        units, placeholder_map = processor.decompile_file(content, file="README.md")

        self.assertIn("Regular paragraph", units)
        protected = [original for _, original in placeholder_map["_MD_PROTECTED"]]
        notes = [original for _, original in placeholder_map["_MD_BLOCK_NOTE"]]
        self.assertIn("---\ntitle: Docs\n---", protected)
        self.assertIn("import Chart from './Chart'", protected)
        self.assertIn("| Name | Value |\n| --- | --- |\n| A | B |", protected)
        self.assertIn("<div>\n  <span>Raw HTML</span>\n</div>", protected)
        self.assertEqual(notes, ["> [!IMPORTANT]"])
        self.assertIn("> Keep this exact.", units)
        self.assertEqual(processor.build_file(units, placeholder_map, "es"), content)

    def test_admonition_marker_is_protected_but_body_is_translatable(self):
        content = (
            "> [!WARNING]\n"
            "> We only use TRANSLATION DeepL\n"
            "> This may affect the quality of the translation."
        )
        processor = Processor()

        units, placeholder_map = processor.decompile_file(content, file="README.md")

        notes = [original for _, original in placeholder_map["_MD_BLOCK_NOTE"]]
        self.assertEqual(notes, ["> [!WARNING]"])
        self.assertIn(
            "> We only use TRANSLATION DeepL\n"
            "> This may affect the quality of the translation.",
            units,
        )
        self.assertEqual(processor.build_file(units, placeholder_map, "ru"), content)

    def test_inline_code_is_protected_inside_translatable_text(self):
        content = "- `FILES`: A comma-separated list of files to translate."
        processor = Processor()

        units, placeholder_map = processor.decompile_file(content, file="README.md")

        protected_inline = [
            original for _, original in placeholder_map["_NON_TRANSLATE"]
        ]
        self.assertEqual(protected_inline, ["`FILES`"])
        self.assertNotIn("`FILES`", units[0])
        self.assertEqual(processor.build_file(units, placeholder_map, "ru"), content)

    def test_github_markdown_fixture_keeps_admonition_body_and_inline_code_safe(self):
        content = Path("tests/fixtures/github_markdown.md").read_text(encoding="utf-8")
        processor = Processor()

        units, placeholder_map = processor.decompile_file(
            content, file="github_markdown.md"
        )

        notes = [original for _, original in placeholder_map["_MD_BLOCK_NOTE"]]
        inline = [original for _, original in placeholder_map["_NON_TRANSLATE"]]
        self.assertEqual(notes, ["> [!WARNING]"])
        self.assertTrue(
            any("Inline code such as" in unit for unit in units),
            "Admonition body should remain in translatable units.",
        )
        self.assertIn("`FILES`", inline)
        links = [original for _, original in placeholder_map["_L1NK"]]
        self.assertIn("`LANGS`", inline)
        self.assertIn("../README.md", links)
        self.assertEqual(processor.build_file(units, placeholder_map, "ru"), content)

    def test_multiline_list_item_is_single_translation_unit(self):
        content = "- first line\n  continuation line\n  - nested item"
        processor = Processor()

        units, _ = processor.decompile_file(content)

        self.assertEqual(units, [content])


if __name__ == "__main__":
    unittest.main()