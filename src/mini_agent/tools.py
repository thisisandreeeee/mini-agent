from pathlib import Path


def list_files(dirpath: str) -> list[str]:
    return [path.name for path in Path(dirpath).iterdir()]


def read_file(filepath: str) -> str:
    return Path(filepath).read_text()
