class LocalizationError(Exception):
    """Base exception for localization workflow errors."""


class InvalidArgumentsError(LocalizationError):
    """Raised when CLI arguments are invalid."""


class InvalidMarkdownFileError(LocalizationError):
    """Raised when provided file does not have .md extension."""


class TranslationFailedError(LocalizationError):
    """Raised when a translation call fails."""


class FileWriteError(LocalizationError):
    """Raised when translated content cannot be written to disk."""
