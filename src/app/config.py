from dataclasses import dataclass


@dataclass(slots=True)
class LocalizationConfig:
    files: str
    langs: str
    debug: str
    max_threads: str = "5"
    max_line_length: str = "500"
    provider: str = "GoogleTranslator"
    source_language: str = "auto"
    provider_options: str = ""
    validate_provider: str = "false"


@dataclass(frozen=True)
class MarkdownRange:
    start: int
    end: int
    kind: str
