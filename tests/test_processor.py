import unittest

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
        self.assertEqual(notes, ["> [!IMPORTANT]\n> Keep this exact."])
        self.assertEqual(processor.build_file(units, placeholder_map, "es"), content)

    def test_multiline_list_item_is_single_translation_unit(self):
        content = "- first line\n  continuation line\n  - nested item"
        processor = Processor()

        units, _ = processor.decompile_file(content)

        self.assertEqual(units, [content])


if __name__ == "__main__":
    unittest.main()