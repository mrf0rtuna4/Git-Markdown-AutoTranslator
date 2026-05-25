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

import asyncio
import sys

from app import LocalizationManager, log_info, log_error
from app.exceptions import InvalidArgumentsError, InvalidMarkdownFileError


def _parse_arguments(argv):
    try:
        files, langs, debug, max_threads, max_line_length = argv[1:6]
    except ValueError as exc:
        raise InvalidArgumentsError(
            "Invalid arguments. Usage: <files> <langs> <debug> <max_threads> <max_line_length>"
        ) from exc
    return files, langs, debug, max_threads, max_line_length

async def main():
    log_info("💚 AutoLocalizator | by mrf0rtuna4")
    try:
        files, langs, debug, max_threads, max_line_length = _parse_arguments(sys.argv)
    except InvalidArgumentsError as exc:
        log_error(f"❌ {exc}")
        sys.exit(1)

    if debug.lower() == 'true':
        import logging
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        for fn in [f.strip() for f in files.split(',')]:
            if not fn.endswith('.md'):
                raise InvalidMarkdownFileError(f"File {fn} is not a markdown file")
    except InvalidMarkdownFileError as exc:
        log_error(f"❌ {exc}")
        sys.exit(1)

    manager = LocalizationManager(
        langs=langs,
        files=files,
        max_line_length=int(max_line_length),
        max_threads=int(max_threads)
    )
    await manager.update_localizations()


if __name__ == '__main__':
    asyncio.run(main())
