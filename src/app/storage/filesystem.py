from pathlib import Path


class FileSystem:
    @staticmethod
    def read_text(path: str) -> str:
        return Path(path).read_text(encoding="utf-8")

    @staticmethod
    def write_text(path: str, content: str) -> None:
        file_path = Path(path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path.write_text(
            content,
            encoding="utf-8",
        )
