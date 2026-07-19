# mini-agent

A barebones Python agent project.

## Setup

Install `uv`:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Create a virtual environment:

```sh
uv venv
```

Install dependencies:

```sh
uv sync
```

Create your local environment file:

```sh
cp .env.example .env
```

Activate the environment:

```sh
source .venv/bin/activate
```

Export environment variables:

```sh
set -a
source .env
set +a
```

## Usage

Start an interactive session:

```sh
python -m mini_agent.main
```

Enter messages at the `You:` prompt. The agent keeps the full conversation context,
including tool calls and results, until you enter `/kill`. You can optionally provide
the first message on the command line:

```sh
python -m mini_agent.main "Hello world"
```

## Evaluation

The RAG evaluation harness runs the committed cases in `fixtures/rag/eval.jsonl`
against a fresh agent conversation. It uses DeepEval with Mistral as both the agent
provider and judge, so it requires `MISTRAL_API_KEY` and incurs API cost.

Install the development dependencies:

```sh
uv sync --group dev
```

Run the credential-free unit tests (the live LLM cases are excluded):

```sh
uv run pytest -m "not llm_eval" -q
```

After exporting the variables in `.env`, run one inexpensive smoke case:

```sh
set -a && source .env && set +a
uv run deepeval test run tests/evals/test_rag_quality.py -k q01 -m llm_eval -v
```

Run the complete 14-case corpus:

```sh
set -a && source .env && set +a
uv run deepeval test run tests/evals/test_rag_quality.py -m llm_eval -v
```

Each case checks answer relevance, faithfulness to the fixture's gold source
context, and correctness against its expected answer. This is an answer-quality
harness, not a retrieval precision/recall benchmark: the current retriever returns
the full corpus. Metrics begin with a `0.7` threshold; inspect DeepEval's failure
reasons before changing a threshold.
