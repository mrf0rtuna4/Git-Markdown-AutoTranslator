from core.app.localizator import LocalizationManager
import asyncio
import sys
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class BlockingTranslator:
    calls = []

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def translate(self, text):
        BlockingTranslator.calls.append(
            (self.target, text, threading.current_thread().name)
        )
        time.sleep(0.2)
        return f"{self.target}:{text}"


class LocalizationManagerTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        BlockingTranslator.calls = []

    async def test_translate_text_runs_blocking_translator_in_executor(self):
        manager = LocalizationManager(langs="es", files=[], max_threads=1)
        try:
            with patch("core.app.localizator.GoogleTranslator", BlockingTranslator):
                started_at = time.perf_counter()
                task = asyncio.create_task(
                    manager.translate_text("hello", "es"))
                await asyncio.sleep(0)
                self.assertLess(time.perf_counter() - started_at, 0.1)

                self.assertEqual(await task, "es:hello")
        finally:
            manager.shutdown()

        self.assertEqual(len(BlockingTranslator.calls), 1)
        _, _, thread_name = BlockingTranslator.calls[0]
        self.assertNotEqual(thread_name, threading.current_thread().name)

    async def test_translate_markdown_unit_preserves_inline_placeholders(self):
        manager = LocalizationManager(langs="ru", files=[], max_threads=1)
        try:
            manager.processor.placeholder_map["_NON_TRANSLATE"] = [
                ("_NON_TRANSLATE_token", "`FILES`")
            ]

            with patch("core.app.localizator.GoogleTranslator", BlockingTranslator):
                translated = await manager.translate_markdown_unit(
                    "- _NON_TRANSLATE_token: A comma-separated list", "ru"
                )
        finally:
            manager.shutdown()

        self.assertEqual(
            translated, "- _NON_TRANSLATE_tokenru:: A comma-separated list"
        )
        translated_segments = [call[1] for call in BlockingTranslator.calls]
        self.assertEqual(translated_segments, [": A comma-separated list"])

    async def test_translate_text_uses_cache(self):
        manager = LocalizationManager(langs="es", files=[], max_threads=1)
        try:
            with patch("core.app.localizator.GoogleTranslator", BlockingTranslator):
                self.assertEqual(
                    await manager.translate_text("hello", "es"), "es:hello"
                )
                self.assertEqual(
                    await manager.translate_text("hello", "es"), "es:hello"
                )
        finally:
            manager.shutdown()

        self.assertEqual(len(BlockingTranslator.calls), 1)


if __name__ == "__main__":
    unittest.main()
