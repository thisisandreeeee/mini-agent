import json

from mistralai.client import Mistral
from loguru import logger
from pprint import pformat

from src.mini_agent import tools

SYSTEM_PROMPT = "You are a helpful assistant with access to tools. If a tool does not help, simply return the response. If you get the same result from multiple tool calls, don't try again."
MODEL = "mistral-small-latest"
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all of the files within a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dirpath": {
                        "type": "string",
                        "description": "The path of the directory.",
                    }
                },
                "required": ["dirpath"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read file contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The filepath to be read.",
                    }
                },
                "required": ["filepath"],
            },
        },
    },
]
TOOL_REGISTRY = {"list_files": tools.list_files, "read_file": tools.read_file}


class Agent:
    def __init__(self, api_key) -> None:
        self.client = Mistral(api_key=api_key)
        self.max_iters = 8

    def run(self, task: str) -> None:
        iter = 0
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task},
        ]
        while iter < self.max_iters:
            response = self.client.chat.complete(
                model=MODEL, messages=messages, tools=TOOLS
            )
            msg = response.choices[0].message
            logger.info(f"{iter=} {msg}")
            if msg.tool_calls is not None:
                if len(msg.tool_calls) > 1:
                    raise NotImplementedError("Multiple tool calls not supported")
                tool = msg.tool_calls[0]
                fname = tool.function.name
                fargs = json.loads(tool.function.arguments)
                try:
                    fn_output = TOOL_REGISTRY[fname](**fargs)
                except Exception as e:
                    fn_output = str(e)
                messages.append(msg)
                messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(fn_output),
                        "name": fname,
                        "tool_call_id": tool.id,
                    }
                )
                logger.info(f"Tool call: {fname} - {fn_output}")
                iter += 1
            else:
                logger.info(f"Exit loop: {msg}")
                return msg
