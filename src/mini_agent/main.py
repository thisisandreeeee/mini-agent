import argparse
import os

from mini_agent.agent import Agent
from mini_agent.tool_registry import DEFAULT_TOOLS
from mistralai.client import Mistral
from loguru import logger


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("task", help="What should the agent do?")
    args = parser.parse_args()

    api_key = os.environ["MISTRAL_API_KEY"]
    logger.info("Start agent run")
    agent = Agent(client=Mistral(api_key=api_key), tools=DEFAULT_TOOLS)
    result = agent.run(args.task)
    logger.info(f"Run complete: {result}")


if __name__ == "__main__":
    main()
