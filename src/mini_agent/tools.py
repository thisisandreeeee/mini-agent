from pathlib import Path


def list_files(dirpath: str) -> list[str]:
    return [path.name for path in Path(dirpath).iterdir()]


def read_file(filepath: str) -> str:
    return Path(filepath).read_text()


def retrieve_kestrel_information(query: str) -> str:
    """Naive RAG implementation using local FS."""
    pardir = "fixtures/rag/docs/"
    results = []
    for f in list_files(pardir):
        text = read_file(pardir + f)
        results.append({"source": pardir + f, "content": text})
    return results
