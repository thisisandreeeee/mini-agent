from pathlib import Path

import pytest

from mini_agent.evals.dataset import EvalCase, load_cases, load_gold_context


def test_load_cases_reads_existing_rag_fixture() -> None:
    cases = load_cases()

    assert len(cases) == 14
    assert len({case.id for case in cases}) == 14
    assert cases[0].id == "q01"
    assert cases[-1].type == "unanswerable"


def test_gold_context_uses_declared_source_documents() -> None:
    case = next(case for case in load_cases() if case.id == "q01")

    context = load_gold_context(case)

    assert len(context) == 1
    assert "Marlin" in context[0]


def test_unanswerable_case_uses_entire_corpus() -> None:
    case = next(case for case in load_cases() if case.id == "q13")

    context = load_gold_context(case)

    assert len(context) == 10
    assert all(context)


def test_load_cases_rejects_missing_required_fields(tmp_path: Path) -> None:
    dataset = tmp_path / "invalid.jsonl"
    dataset.write_text('{"id": "bad"}\n', encoding="utf-8")

    with pytest.raises(ValueError, match="missing"):
        load_cases(dataset)


def test_gold_context_reports_missing_declared_source(tmp_path: Path) -> None:
    case = EvalCase(
        id="missing-source",
        question="question",
        expected_answer="answer",
        sources=("missing.md",),
        type="single-hop",
    )

    with pytest.raises(FileNotFoundError, match="missing-source"):
        load_gold_context(case, tmp_path)
