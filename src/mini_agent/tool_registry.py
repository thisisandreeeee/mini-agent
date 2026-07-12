from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from . import tools


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: Callable[..., Any]

    @property
    def schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


DEFAULT_TOOLS = [
    Tool(
        name="list_files",
        description="List all of the files within a directory.",
        parameters={
            "type": "object",
            "properties": {
                "dirpath": {
                    "type": "string",
                    "description": "The path of the directory.",
                }
            },
            "required": ["dirpath"],
        },
        handler=tools.list_files,
    ),
    Tool(
        name="read_file",
        description="Read file contents.",
        parameters={
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "The filepath to be read.",
                }
            },
            "required": ["filepath"],
        },
        handler=tools.read_file,
    ),
]
