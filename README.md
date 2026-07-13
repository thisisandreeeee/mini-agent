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
