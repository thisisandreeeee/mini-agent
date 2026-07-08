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
uv pip install -r requirements.txt
```

Activate the environment:

```sh
source .venv/bin/activate
```

## Usage

Run the agent with a task:

```sh
python -m mini_agent.main "xyz"
```

Add dependencies later by editing `requirements.txt`, then rerun:

```sh
uv pip install -r requirements.txt
```
