import argparse

from mini_agent.agent import Agent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("task", help="What should the agent do?")
    args = parser.parse_args()

    agent = Agent()
    agent.run(args.task)


if __name__ == "__main__":
    main()
