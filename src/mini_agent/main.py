import argparse
import os

from mini_agent.agent import Agent
from mini_agent.tool_registry import DEFAULT_TOOLS
from mistralai.client import Mistral
from loguru import logger


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("task", nargs="?", help="Optional first message")
    args = parser.parse_args()

    api_key = os.environ["MISTRAL_API_KEY"]
    agent = Agent(client=Mistral(api_key=api_key), tools=DEFAULT_TOOLS)
    pending_message = args.task

    print("Interactive agent started. Type /kill to exit.")
    try:
        while True:
            if pending_message is None:
                pending_message = input("You: ").strip()

            if pending_message.lower() in {"/kill", "kill"}:
                break
            if not pending_message:
                pending_message = None
                continue

            logger.info("Start agent turn")
            response = agent.chat(pending_message)
            print(f"Agent: {response.content}")
            pending_message = None
    except (EOFError, KeyboardInterrupt):
        print()

    print("Agent stopped.")


if __name__ == "__main__":
    main()
