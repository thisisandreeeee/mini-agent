import asyncio
from types import SimpleNamespace

import pytest
from pydantic import BaseModel

from mini_agent.evals.mistral_judge import MistralJudge


class JudgeVerdict(BaseModel):
    score: int


class FakeChat:
    def __init__(self) -> None:
        self.complete_calls: list[dict[str, object]] = []
        self.parse_calls: list[dict[str, object]] = []

    def complete(self, **kwargs: object) -> object:
        self.complete_calls.append(kwargs)
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="  judge text  "))]
        )

    def parse(self, **kwargs: object) -> object:
        self.parse_calls.append(kwargs)
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(parsed={"score": 1}))]
        )


class FakeMistralClient:
    def __init__(self) -> None:
        self.chat = FakeChat()


def test_generate_returns_normalized_text() -> None:
    client = FakeMistralClient()
    judge = MistralJudge(client=client, model_name="judge-model")  # type: ignore[arg-type]

    assert judge.generate("Score this") == "judge text"
    assert client.chat.complete_calls == [
        {
            "model": "judge-model",
            "messages": [{"role": "user", "content": "Score this"}],
            "temperature": 0.0,
        }
    ]


def test_generate_uses_mistral_structured_output() -> None:
    client = FakeMistralClient()
    judge = MistralJudge(client=client, model_name="judge-model")  # type: ignore[arg-type]

    result = judge.generate("Score this", schema=JudgeVerdict)

    assert result == JudgeVerdict(score=1)
    assert client.chat.parse_calls == [
        {
            "model": "judge-model",
            "messages": [{"role": "user", "content": "Score this"}],
            "response_format": JudgeVerdict,
            "temperature": 0.0,
        }
    ]


def test_a_generate_delegates_to_generate() -> None:
    client = FakeMistralClient()
    judge = MistralJudge(client=client, model_name="judge-model")  # type: ignore[arg-type]

    assert asyncio.run(judge.a_generate("Score this")) == "judge text"


def test_generate_rejects_empty_structured_output() -> None:
    client = FakeMistralClient()
    client.chat.parse = lambda **_: SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(parsed=None))]
    )
    judge = MistralJudge(client=client, model_name="judge-model")  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="no parsed structured output"):
        judge.generate("Score this", schema=JudgeVerdict)
