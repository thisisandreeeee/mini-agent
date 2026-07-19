"""Mistral-backed DeepEval judge model."""

from __future__ import annotations

import os
from typing import Any

from deepeval.models import DeepEvalBaseLLM
from mistralai.client import Mistral
from pydantic import BaseModel

DEFAULT_EVAL_MODEL = "mistral-small-latest"


class MistralJudge(DeepEvalBaseLLM):
    """Adapt Mistral's chat API to DeepEval's custom-model interface."""

    def __init__(self, client: Mistral, model_name: str | None = None) -> None:
        self.client = client
        self.model_name = model_name or os.getenv("MISTRAL_EVAL_MODEL", DEFAULT_EVAL_MODEL)
        super().__init__(model=self.model_name)

    def load_model(self) -> Mistral:
        return self.client

    def get_model_name(self) -> str:
        return self.model_name

    def generate(
        self, prompt: str, schema: type[BaseModel] | None = None
    ) -> str | BaseModel:
        """Generate a judge response, enforcing a schema when DeepEval supplies one."""
        messages = [{"role": "user", "content": prompt}]
        if schema is None:
            response = self.client.chat.complete(
                model=self.model_name,
                messages=messages,
                temperature=0.0,
            )
            return _message_content(response.choices[0].message.content)

        response = self.client.chat.parse(
            model=self.model_name,
            messages=messages,
            response_format=schema,
            temperature=0.0,
        )
        parsed = response.choices[0].message.parsed
        if parsed is None:
            raise ValueError("Mistral returned no parsed structured output for DeepEval")
        if isinstance(parsed, schema):
            return parsed
        return schema.model_validate(parsed)

    async def a_generate(
        self, prompt: str, schema: type[BaseModel] | None = None
    ) -> str | BaseModel:
        """Async DeepEval hook; the SDK's synchronous client is reused safely."""
        return self.generate(prompt, schema=schema)


def _message_content(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        text = "".join(
            part.text
            for part in content
            if getattr(part, "type", None) == "text" and isinstance(part.text, str)
        )
        if text.strip():
            return text.strip()
    raise ValueError("Mistral returned an empty or non-text judge response")
