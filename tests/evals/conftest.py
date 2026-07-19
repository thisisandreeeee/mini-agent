from __future__ import annotations

import os
from collections.abc import Callable

import pytest
from mistralai.client import Mistral

from mini_agent.agent import Agent
from mini_agent.evals.mistral_judge import MistralJudge
from mini_agent.tool_registry import DEFAULT_TOOLS


@pytest.fixture(autouse=True)
def deny_unexpected_tool_approval(monkeypatch: pytest.MonkeyPatch) -> None:
    """Avoid blocking a test if the model unexpectedly selects an approved tool."""
    monkeypatch.setattr("builtins.input", lambda _: "n")


@pytest.fixture
def agent_factory() -> Callable[[], Agent]:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        pytest.skip("MISTRAL_API_KEY is required for live LLM evaluation")

    def create_agent() -> Agent:
        return Agent(client=Mistral(api_key=api_key), tools=DEFAULT_TOOLS)

    return create_agent


@pytest.fixture(scope="session")
def judge() -> MistralJudge:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        pytest.skip("MISTRAL_API_KEY is required for live LLM evaluation")
    return MistralJudge(client=Mistral(api_key=api_key))
