import json
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from mini_agent.agent import Agent
from mini_agent.tool_registry import Tool


def message(*tool_calls):
    return SimpleNamespace(tool_calls=list(tool_calls))


def tool_call(name: str, arguments: str, call_id: str = "call-1"):
    return SimpleNamespace(
        id=call_id,
        function=SimpleNamespace(name=name, arguments=arguments),
    )


def client_with_messages(*messages):
    client = Mock()
    client.chat.complete.side_effect = [
        SimpleNamespace(choices=[SimpleNamespace(message=item)]) for item in messages
    ]
    return client


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.handler = Mock(return_value=["one.txt"])
        self.tool = Tool(
            name="list_files",
            description="List files.",
            parameters={"type": "object"},
            handler=self.handler,
        )

    def test_returns_first_message_without_tool_calls(self):
        final_message = message()
        agent = Agent(client_with_messages(final_message), [self.tool])

        self.assertIs(agent.run("List files"), final_message)

    def test_executes_multiple_tool_calls_in_one_iteration(self):
        first_call = tool_call("list_files", '{"dirpath": "."}', "call-1")
        second_call = tool_call("list_files", '{"dirpath": "src"}', "call-2")
        final_message = message()
        client = client_with_messages(message(first_call, second_call), final_message)

        result = Agent(client, [self.tool]).run("List files")

        self.assertIs(result, final_message)
        self.assertEqual(
            self.handler.call_args_list,
            [unittest.mock.call(dirpath="."), unittest.mock.call(dirpath="src")],
        )
        sent_messages = client.chat.complete.call_args_list[1].kwargs["messages"]
        tool_messages = sent_messages[-2:]
        self.assertEqual([item["tool_call_id"] for item in tool_messages], ["call-1", "call-2"])
        self.assertEqual(json.loads(tool_messages[0]["content"]), {"result": ["one.txt"]})

    def test_returns_tool_error_to_model(self):
        call = tool_call("unknown", "not-json")
        client = client_with_messages(message(call), message())

        Agent(client, [self.tool]).run("Use a tool")

        sent_messages = client.chat.complete.call_args_list[1].kwargs["messages"]
        self.assertIn("error", json.loads(sent_messages[-1]["content"]))

    def test_raises_when_iteration_limit_is_reached(self):
        call = tool_call("list_files", '{"dirpath": "."}')
        agent = Agent(client_with_messages(message(call)), [self.tool], max_iterations=1)

        with self.assertRaisesRegex(RuntimeError, "exceeded the limit"):
            agent.run("Keep going")


if __name__ == "__main__":
    unittest.main()
