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
from pathlib import Path
from typing import Sequence

# DO NOT MOVE, THIS MAY STAY BEFORE core.* IMPORTS
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.app.exceptions import InvalidArgumentsError, InvalidMarkdownFileError
from core.app import LocalizationManager, LocalizationConfig, Logger, TranslationProviderFactory


def _parse_arguments(argv: Sequence[str]) -> LocalizationConfig:
    try:
        (
            files,
            langs,
            debug,
            max_threads,
            max_line_length,
            *optional_args,
        ) = argv[1:]
    except ValueError as exc:
        raise InvalidArgumentsError(
            "Invalid arguments. Usage: <files> <langs> <debug> "
            "<max_threads> <max_line_length> "
            "[provider] [source_language] [provider_options] "
            "[validate_provider]"
        ) from exc

    if len(optional_args) > 4:
        raise InvalidArgumentsError(
            "Invalid arguments. Usage: <files> <langs> <debug> "
            "<max_threads> <max_line_length> "
            "[provider] [source_language] [provider_options] "
            "[validate_provider]"
        )

    provider: str = (
        optional_args[0]
        if len(optional_args) >= 1
        else "GoogleTranslator"
    )

    source_language: str = (
        optional_args[1]
        if len(optional_args) >= 2
        else "auto"
    )

    provider_options: str = (
        optional_args[2]
        if len(optional_args) >= 3
        else ""
    )

    validate_provider: str = (
        optional_args[3]
        if len(optional_args) >= 4
        else "false"
    )

    try:
        TranslationProviderFactory.canonical_name(provider)
    except ValueError as exc:
        raise InvalidArgumentsError(str(exc)) from exc

    return LocalizationConfig(
        files=files,
        langs=langs,
        debug=debug,
        max_threads=max_threads,
        max_line_length=max_line_length,
        provider=provider,
        source_language=source_language,
        provider_options=provider_options,
        validate_provider=validate_provider,
    )


def str_to_bool(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes", "on"}


async def main():
    logger = Logger()
    logger.log_info("💚 AutoLocalizator | by mrf0rtuna4")

    try:
        args = _parse_arguments(sys.argv)
    except InvalidArgumentsError as exc:
        logger.log_error(f"❌ {exc}")
        sys.exit(1)

    if str_to_bool(args.debug):
        import logging

        logging.getLogger().setLevel(logging.DEBUG)

    try:
        for fn in (f.strip() for f in args.files.split(",")):
            if not fn.endswith(".md"):
                raise InvalidMarkdownFileError(
                    f"File {fn} is not a markdown file")
    except InvalidMarkdownFileError as exc:
        logger.log_error(f"❌ {exc}")
        sys.exit(1)

    manager = LocalizationManager(
        files=args.files,
        langs=args.langs,
        max_threads=int(args.max_threads),
        max_line_length=int(args.max_line_length),
        provider=args.provider,
        source_language=args.source_language,
        provider_options=args.provider_options,
    )
    if str_to_bool(args.validate_provider):
        await manager.validate_provider()
    await manager.update_localizations()


if __name__ == "__main__":
    asyncio.run(main())
