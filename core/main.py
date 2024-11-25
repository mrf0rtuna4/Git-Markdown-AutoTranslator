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

import asyncio
import os

from dotenv import load_dotenv

from app import LocalizationManager, log_info, log_error

load_dotenv()


async def main():
    log_info("💚 AutoLocalizator | by mrf0rtuna4")
    selected_langs = os.getenv("LANGS")
    files = os.getenv("FILES")
    max_line_length = os.getenv("MAX_LINELENTH_")

    if not selected_langs or not files:
        log_error("❌ Environment variable(s) not set. Check the LANGS and FILES in env")
        return

    for filename in [file.strip() for file in files.split(",")] if isinstance(files, str) else files:
        if not filename.endswith(".md"):
            log_error(f"❌ File {filename} not supported because it's not a markdown file")
            return

    if max_line_length is None:
        max_line_length = 500

    manager = LocalizationManager(selected_langs, files, int(max_line_length))
    await manager.update_localizations()


if __name__ == "__main__":
    asyncio.run(main())
