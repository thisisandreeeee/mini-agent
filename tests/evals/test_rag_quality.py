from __future__ import annotations

from typing import Any

import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, GEval
from deepeval.test_case import LLMTestCase, SingleTurnParams

from mini_agent.evals.dataset import EvalCase, load_cases, load_gold_context
from mini_agent.evals.mistral_judge import MistralJudge


@pytest.mark.llm_eval
@pytest.mark.parametrize("case", load_cases(), ids=lambda case: case.id)
def test_rag_answer_quality(
    case: EvalCase,
    agent_factory: Any,
    judge: MistralJudge,
) -> None:
    """Evaluate a fresh agent response against each committed RAG case."""
    response = agent_factory().run(case.question)
    actual_output = _response_text(response.content)
    test_case = LLMTestCase(
        input=case.question,
        actual_output=actual_output,
        expected_output=case.expected_answer,
        retrieval_context=load_gold_context(case),
    )
    metrics = [
        AnswerRelevancyMetric(model=judge, threshold=0.7),
        FaithfulnessMetric(model=judge, threshold=0.7),
        GEval(
            name="Expected Answer Correctness",
            criteria=(
                "Judge whether the actual answer correctly answers the input using "
                "the expected answer as the reference. For unanswerable references, "
                "the answer must clearly decline to invent a fact."
            ),
            evaluation_params=[
                SingleTurnParams.INPUT,
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.EXPECTED_OUTPUT,
            ],
            model=judge,
            threshold=0.7,
        ),
    ]

    assert_test(test_case, metrics)


def _response_text(content: Any) -> str:
    if isinstance(content, str) and content.strip():
        return content.strip()
    if isinstance(content, list):
        text = "".join(
            part.text
            for part in content
            if getattr(part, "type", None) == "text" and isinstance(part.text, str)
        )
        if text.strip():
            return text.strip()
    raise AssertionError("Agent returned an empty or non-text response")
