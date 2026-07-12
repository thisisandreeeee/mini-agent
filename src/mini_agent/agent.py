import json
from typing import Any

from loguru import logger
from mistralai.client import Mistral

from .tool_registry import Tool

SYSTEM_PROMPT = (
    "You are a helpful assistant with access to tools. If a tool does not help, "
    "simply return the response. If you get the same result from multiple tool "
    "calls, don't try again."
)
MODEL = "mistral-small-latest"


class Agent:
    def __init__(
        self,
        client: Mistral,
        tools: list[Tool],
        model: str = MODEL,
        system_prompt: str = SYSTEM_PROMPT,
        max_iterations: int = 8,
    ) -> None:
        self.client = client
        self.tools = {tool.name: tool for tool in tools}
        self.model = model
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations

    def run(self, task: str) -> Any:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": task},
        ]

        for iteration in range(self.max_iterations):
            message = self._complete(messages)
            logger.info("iteration={} message={}", iteration, message)

            if not message.tool_calls:
                return message

            messages.append(message)
            for tool_call in message.tool_calls:
                tool_message = self._execute_tool_call(tool_call)
                messages.append(tool_message)

        raise RuntimeError(
            f"Agent exceeded the limit of {self.max_iterations} tool iterations"
        )

    def _complete(self, messages: list[Any]) -> Any:
        response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            tools=[tool.schema for tool in self.tools.values()],
        )
        return response.choices[0].message

    def _execute_tool_call(self, tool_call: Any) -> dict[str, Any]:
        name = tool_call.function.name

        try:
            arguments = json.loads(tool_call.function.arguments)
            output = self.tools[name].handler(**arguments)
            content = {"result": output}
            logger.info("Tool call: {} - {}", name, output)
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            content = {"error": str(error)}
            logger.warning("Invalid tool call: {} - {}", name, error)
        except Exception as error:
            content = {"error": str(error)}
            logger.exception("Tool execution failed: {}", name)

        return {
            "role": "tool",
            "content": json.dumps(content),
            "name": name,
            "tool_call_id": tool_call.id,
        }
