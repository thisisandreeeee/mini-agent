"""Load the repository's RAG evaluation fixtures."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATASET_PATH = PROJECT_ROOT / "fixtures" / "rag" / "eval.jsonl"
DEFAULT_DOCS_DIR = PROJECT_ROOT / "fixtures" / "rag" / "docs"


@dataclass(frozen=True)
class EvalCase:
    """One expected RAG interaction from the JSONL evaluation fixture."""

    id: str
    question: str
    expected_answer: str
    sources: tuple[str, ...]
    type: str


def load_cases(dataset_path: Path = DEFAULT_DATASET_PATH) -> list[EvalCase]:
    """Parse validated cases from the JSONL evaluation fixture."""
    try:
        lines = dataset_path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Evaluation dataset not found: {dataset_path}") from error

    cases: list[EvalCase] = []
    seen_ids: set[str] = set()
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Invalid JSON in evaluation dataset at line {line_number}: {dataset_path}"
            ) from error
        case = _parse_case(payload, line_number, dataset_path)
        if case.id in seen_ids:
            raise ValueError(f"Duplicate evaluation case id {case.id!r} in {dataset_path}")
        seen_ids.add(case.id)
        cases.append(case)
    return cases


def load_gold_context(
    case: EvalCase, docs_dir: Path = DEFAULT_DOCS_DIR
) -> list[str]:
    """Return gold source content used to assess an answer's grounding.

    Unanswerable cases intentionally use the complete corpus, allowing the judge to
    confirm that the requested fact is absent rather than expecting a source file.
    """
    source_paths = (
        [docs_dir / source for source in case.sources]
        if case.sources
        else sorted(docs_dir.glob("*.md"))
    )
    context: list[str] = []
    for path in source_paths:
        try:
            context.append(path.read_text(encoding="utf-8"))
        except FileNotFoundError as error:
            raise FileNotFoundError(
                f"Source document for evaluation case {case.id!r} not found: {path}"
            ) from error
    return context


def _parse_case(payload: Any, line_number: int, dataset_path: Path) -> EvalCase:
    if not isinstance(payload, dict):
        raise ValueError(
            f"Evaluation dataset line {line_number} in {dataset_path} must be an object"
        )

    required_fields = ("id", "question", "expected_answer", "sources", "type")
    missing = [field for field in required_fields if field not in payload]
    if missing:
        raise ValueError(
            f"Evaluation dataset line {line_number} in {dataset_path} is missing: "
            f"{', '.join(missing)}"
        )

    text_fields = ("id", "question", "expected_answer", "type")
    invalid_fields = [
        field for field in text_fields if not isinstance(payload[field], str) or not payload[field]
    ]
    if invalid_fields or not isinstance(payload["sources"], list) or not all(
        isinstance(source, str) and source for source in payload["sources"]
    ):
        raise ValueError(
            f"Evaluation dataset line {line_number} in {dataset_path} has invalid fields"
        )

    return EvalCase(
        id=payload["id"],
        question=payload["question"],
        expected_answer=payload["expected_answer"],
        sources=tuple(payload["sources"]),
        type=payload["type"],
    )
