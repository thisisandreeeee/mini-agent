import json
from typing import Any

from loguru import logger
from mistralai.client import Mistral

from .tool_registry import Tool

SYSTEM_PROMPT = """You are a helpful assistant with access to tools."""
MODEL = "mistral-small-latest"


class Agent:
    def __init__(
        self,
        client: Mistral,
        tools: list[Tool],
        model: str = MODEL,
        system_prompt: str = SYSTEM_PROMPT,
        max_iterations: int = 5,
    ) -> None:
        self.client = client
        self.tools = {tool.name: tool for tool in tools}
        self.model = model
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations

    def run(self, task: str) -> Any:
        self.tool_call_counter = {}
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

        messages.append(
            {
                "role": "user",
                "content": "You have reached the maximum allowable iterations. Do not call another tool. Explain why the available tools could not complete the task and summarise any repeated unsuccessful approach.",
            }
        )
        return self._complete(messages)

    def _complete(self, messages: list[Any]) -> Any:
        response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            tools=[tool.schema for tool in self.tools.values()],
            temperature=0.0,
        )
        return response.choices[0].message

    def _execute_tool_call(self, tool_call: Any) -> dict[str, Any]:
        name = tool_call.function.name
        arguments = tool_call.function.arguments

        key = (name, arguments)
        if key not in self.tool_call_counter:
            self.tool_call_counter[key] = 0

        if self.tool_call_counter[key] >= 1:
            return {
                "role": "tool",
                "content": json.dumps(
                    {
                        "error": f"This exact tool has been called {self.tool_call_counter[key]} times with the same argument and provided no new information. Do not call it again. Explain why the available tools cannot complete the task."
                    }
                ),
                "name": name,
                "tool_call_id": tool_call.id,
            }

        try:
            output = self.tools[name].handler(**json.loads(arguments))
            content = {"result": output}
            logger.info("Tool call: {} - {}", name, output)
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            content = {"error": str(error)}
            logger.warning("Invalid tool call: {} - {}", name, error)
        except Exception as error:
            content = {"error": str(error)}
            logger.exception("Tool execution failed: {}", name)

        self.tool_call_counter[key] += 1
        return {
            "role": "tool",
            "content": json.dumps(content),
            "name": name,
            "tool_call_id": tool_call.id,
        }
