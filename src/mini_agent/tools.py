import os


def list_files(dirpath: str) -> str:
    return str(os.listdir(dirpath))


def read_file(filepath: str) -> str:
    with open(filepath, "r") as f:
        return f.read()
