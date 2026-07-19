import os
import json
from dataclasses import dataclass

from deepeval import assert_test
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import GEval
from mistralai.client import Mistral

from mini_agent.agent import Agent
from mini_agent.evals.mistral_judge import MistralJudge
from mini_agent.tool_registry import DEFAULT_TOOLS


@dataclass
class EvalCase:
    id: str
    question: str
    expected_answer: str
    sources: list[str]
    type: str

    @classmethod
    def from_dict(self, eval):
        return EvalCase(
            eval["id"],
            eval["question"],
            eval["expected_answer"],
            eval["sources"],
            eval["type"],
        )


def test_rag():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    agent = Agent(client, tools=DEFAULT_TOOLS)
    judge = MistralJudge(client)

    with open("fixtures/rag/eval.jsonl", "r") as f:
        evals = [json.loads(line) for line in list(f)]

    metrics = [
        GEval(
            name="Factuality",
            criteria="Determine if the 'actual output' is factually correct based on the 'expected output'. Test for meaning, rather than strict adherence.",
            evaluation_params=[
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.EXPECTED_OUTPUT,
            ],
            threshold=0.5,
            model=judge,
        )
    ]

    for eval in evals:
        eval_case = EvalCase.from_dict(eval)
        response = agent.chat(eval_case.question)
        test_case = LLMTestCase(
            input=eval_case.question,
            actual_output=response.content,
            expected_output=eval_case.expected_answer,
        )
        assert_test(test_case, metrics)
