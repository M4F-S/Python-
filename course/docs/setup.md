# Setup

## Prerequisites

- Python 3.10 or newer
- `pip`, or `uv`, or `poetry` — any one is fine
- git

## With `uv` (fastest, recommended)

```bash
cd course
uv sync
source .venv/bin/activate
```

## With plain `pip`

```bash
cd course
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .      # installs the `course` CLI
```

## With `poetry`

```bash
cd course
poetry install
poetry shell
```

## Verify

```bash
python --version               # 3.10+
python -c "import pydantic; print(pydantic.VERSION)"
course status                  # lists every module
pytest tests/ -q               # 39 solution tests should pass
```
