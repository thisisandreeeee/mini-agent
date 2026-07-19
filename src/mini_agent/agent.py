import json
from typing import Any

from loguru import logger
from mistralai.client import Mistral

from .tool_registry import Tool

SYSTEM_PROMPT = """You are a helpful assistant for Kestrel Analytics.

In this environment you have access to a set of tools you can use to answer the user's question.
Whenever you state a fact, you must cite your source.
"""
MODEL = "mistral-small-latest"
MAX_LOG_LENGTH = 300


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
        self.messages: list[Any] = []
        self.reset()

    def reset(self) -> None:
        """Start a new conversation."""
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def chat(self, message: str) -> Any:
        """Send one message while preserving context from earlier turns."""
        self.tool_call_counter = {}
        self.messages.append({"role": "user", "content": message})

        for iteration in range(self.max_iterations):
            response_message = self._complete(self.messages)
            logger.info("iteration={} message={}", iteration, response_message)
            self.messages.append(response_message)

            if not response_message.tool_calls:
                return response_message

            for tool_call in response_message.tool_calls:
                tool_message, tool_ok = self._execute_tool_call(tool_call)
                self.messages.append(tool_message)
                if not tool_ok:
                    self.messages.append(
                        {
                            "role": "user",
                            "content": "The tool call failed. Clearly explain the error to the user, including what went wrong and any relevant error details. Do not attempt to answer the original question because the required information was not retrieved. Where appropriate, suggest what the user can do next.",
                        }
                    )
                    err_message = self._complete(self.messages)
                    return err_message

        self.messages.append(
            {
                "role": "user",
                "content": "You have reached the maximum allowable iterations. Do not call another tool. Explain why the available tools could not complete the task and summarise any repeated unsuccessful approach.",
            }
        )
        response_message = self._complete(self.messages)
        self.messages.append(response_message)
        return response_message

    def _complete(self, messages: list[Any]) -> Any:
        response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            tools=[tool.schema for tool in self.tools.values()],
            temperature=0.0,
        )
        return response.choices[0].message

    def _execute_tool_call(self, tool_call: Any) -> dict[str, Any]:
        ok = False
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
            }, ok

        try:
            if self.tools[name].requires_approval:
                approval_text = input(
                    f"Approval required to execute {name} with {arguments=}.\nProceed? [y/N]"
                )
                if approval_text.strip().lower() != "y":
                    raise Exception(f"Approval not granted for tool_call {name}.")
            output = self.tools[name].handler(**json.loads(arguments))
            content = {"result": output}
            logger.info("Tool call: {} - {}", name, output[:MAX_LOG_LENGTH])
            ok = True
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
        }, ok
