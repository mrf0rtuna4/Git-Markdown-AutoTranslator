import os
import sys
import unittest

from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.app.providers import ProviderSpec, TranslationProviderFactory


class RecordingTranslator:
    calls = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        RecordingTranslator.calls.append(kwargs)

    def translate(self, text):
        return f"{self.kwargs['target']}:{text}"


class TranslationProviderFactoryTests(unittest.TestCase):
    def setUp(self):
        RecordingTranslator.calls = []
        self.provider_patch = patch.dict(
            TranslationProviderFactory._PROVIDERS,
            {
                "recording": ProviderSpec(
                    "RecordingTranslator",
                    RecordingTranslator,
                    {
                        "api_key": "RECORDING_API_KEY",
                        "use_free_api": "RECORDING_USE_FREE_API",
                    },
                    {"use_free_api": False},
                )
            },
        )
        self.provider_patch.start()

    def tearDown(self):
        self.provider_patch.stop()

    def test_build_uses_source_target_defaults_and_environment_options(self):
        with patch.dict(
            os.environ,
            {"RECORDING_API_KEY": "secret", "RECORDING_USE_FREE_API": "true"},
        ):
            translator = TranslationProviderFactory.build(
                provider="recording", source="en", target="es"
            )

        self.assertEqual(translator.translate("hello"), "es:hello")
        self.assertEqual(
            RecordingTranslator.calls[0],
            {
                "source": "en",
                "target": "es",
                "use_free_api": True,
                "api_key": "secret",
            },
        )

    def test_build_allows_json_provider_options_to_override_environment(self):
        with patch.dict(os.environ, {"RECORDING_API_KEY": "secret"}):
            TranslationProviderFactory.build(
                provider="recording",
                source="en",
                target="de",
                provider_options='{"api_key": "override", "custom_url": "http://local"}',
            )

        self.assertEqual(
            RecordingTranslator.calls[0],
            {
                "source": "en",
                "target": "de",
                "use_free_api": False,
                "api_key": "override",
                "custom_url": "http://local",
            },
        )

    def test_unknown_provider_lists_available_providers(self):
        with self.assertRaisesRegex(ValueError, "Unsupported translation provider"):
            TranslationProviderFactory.canonical_name("unknown")


if __name__ == "__main__":
    unittest.main()