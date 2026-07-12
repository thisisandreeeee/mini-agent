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

Run the agent with a task:

```sh
python -m mini_agent.main "Hello world"
```
