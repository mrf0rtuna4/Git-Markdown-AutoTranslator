import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.app.exceptions import InvalidArgumentsError
from core.main import _parse_arguments


class MainArgumentParsingTests(unittest.TestCase):
    def test_parse_arguments_keeps_backwards_compatible_defaults(self):
        config = _parse_arguments(
            ["main.py", "README.md", "es", "false", "5", "500"]
        )

        self.assertEqual(config.provider, "GoogleTranslator")
        self.assertEqual(config.source_language, "auto")
        self.assertEqual(config.provider_options, "")
        self.assertEqual(config.validate_provider, "false")

    def test_parse_arguments_accepts_provider_options(self):
        config = _parse_arguments(
            [
                "main.py",
                "README.md",
                "de",
                "false",
                "2",
                "1000",
                "deepl",
                "en",
                '{"api_key": "secret"}',
                "true",
            ]
        )

        self.assertEqual(config.provider, "deepl")
        self.assertEqual(config.source_language, "en")
        self.assertEqual(config.provider_options, '{"api_key": "secret"}')
        self.assertEqual(config.validate_provider, "true")

    def test_parse_arguments_rejects_unknown_provider(self):
        with self.assertRaises(InvalidArgumentsError):
            _parse_arguments(
                ["main.py", "README.md", "es", "false", "5", "500", "unknown"]
            )


if __name__ == "__main__":
    unittest.main()