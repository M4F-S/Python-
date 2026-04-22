# Module 08 — Virtualenvs & Packaging (The Matrix)

> *"Every installed package is a commitment."*

This module is the first where the code itself is short — the learning is
in the workflow: how to isolate Python environments, how to pin
dependencies, how to keep secrets out of source. Coming from C, the
mental model to drop is "one global compiler with one standard library."
Python runs against the interpreter's install, and installing a package
edits that install. Virtual environments let you pretend otherwise.

## 1. Virtual environments (`venv`)

A virtual environment is a directory containing:
- A copy (or symlink) of the Python interpreter.
- An empty `site-packages/`.
- Activation scripts that tweak `PATH` so `python3` / `pip` resolve
  inside the env instead of the system.

```
$ python3 -m venv .venv             # create
$ source .venv/bin/activate         # "enter" the env
(.venv) $ pip install pandas        # installed inside .venv only
(.venv) $ deactivate                # leave
```

How to tell if you're in one inside Python (this is what Exercise 0
asks for):

```python
import sys
in_venv = sys.prefix != sys.base_prefix
```

- `sys.prefix` — root of the interpreter *currently running*.
- `sys.base_prefix` — root of the interpreter the venv was built from.
  They differ if and only if you're inside a venv.
- `sys.executable` — path to the running interpreter binary.
- `os.environ.get("VIRTUAL_ENV")` — set by the activation script; useful
  for the env's name (`os.path.basename(...)`).

Why bother?
- Projects pin different versions of the same library.
- The system Python is shared with the OS; `pip install`ing into it can
  break `apt` or `yum` machinery.
- Recreating a venv from `requirements.txt` gives you repeatable builds.

## 2. `pip` and `requirements.txt`

Bare minimum:

```
$ pip install -r requirements.txt
```

`requirements.txt` is a plain text list, one package per line, pinning
versions with `==`:

```
pandas==2.1.0
numpy==1.25.0
matplotlib==3.7.2
```

- `pip freeze > requirements.txt` dumps what you currently have.
- `pip show <pkg>` prints the version and install location.
- `importlib.metadata.version("pandas")` reads a package version from
  Python (no shelling out to `pip`).

### `requirements.txt` vs. `pyproject.toml`

- `requirements.txt` is what Python originally shipped with — simple, but
  doesn't record *why* you installed each dep.
- `pyproject.toml` (PEP 517/518/621) is the modern answer. It declares
  metadata (name, version, description), direct dependencies, optional
  dev/test dependencies, and a build backend. Tools like **Poetry**,
  `hatch`, `pdm`, and plain `pip` all read it.
- Poetry additionally maintains a `poetry.lock` with exact transitive
  versions — the same role `package-lock.json` plays for npm.

Minimal `pyproject.toml` using Poetry:

```toml
[tool.poetry]
name = "matrix-loader"
version = "0.1.0"
description = ""
authors = []

[tool.poetry.dependencies]
python = "^3.10"
pandas = "^2.1.0"
numpy = "^1.25.0"
matplotlib = "^3.7.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### Version specifiers in 30 seconds

- `==1.2.3` — exact.
- `>=1.2,<2` — compatible range.
- `^1.2.3` (Poetry) — `>=1.2.3,<2.0.0` (keep major).
- `~=1.2.3` (pip / PEP 440) — `>=1.2.3,<1.3.0` (keep major.minor).

## 3. Environment variables and `.env` files

Secrets (API keys, DB URLs) must never sit in source. Standard pattern:

1. The app reads them from `os.environ`.
2. A local `.env` file holds development values — kept *out* of git.
3. A committed `.env.example` documents which keys are expected, with
   placeholder values.
4. In production, values are injected by the orchestrator (systemd,
   docker-compose, Kubernetes Secrets, CI runner).

`python-dotenv` loads a `.env` into `os.environ`:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # reads ./.env if present
mode = os.environ.get("MATRIX_MODE", "development")
```

`load_dotenv()` does NOT override real environment variables by default,
which is exactly what you want — CLI invocations like
`MATRIX_MODE=production python3 oracle.py` should win.

### `.gitignore` hygiene

```
# virtual envs
.venv/
venv/
matrix_env/

# secrets
.env
*.env
!.env.example

# bytecode / caches
__pycache__/
*.py[cod]
.mypy_cache/
.pytest_cache/
```

`!.env.example` keeps the template committed while everything matching
`*.env` is ignored.

## 4. Graceful handling of missing deps

Exercise 1 deliberately asks the script to work when pandas, numpy, and
matplotlib are *not* installed. The shape:

```python
try:
    import pandas  # noqa: F401
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
```

Then check the flag at the top of your report before doing work that
needs the library. Tell the user which command fixes the missing pieces
(`pip install -r requirements.txt` or `poetry install`).

> The subject permits flake8/mypy errors here *only* for import-related
> lines. Real-world style: wrap the import in `try/except ImportError`
> and reuse a sentinel, exactly as above.

## 5. Peer-review angle

When your classmate asks "why venv?", you want a one-line answer:

> Because installing a package edits the interpreter's site-packages
> globally. A venv gives every project its own site-packages, so two
> projects can pin different versions without fighting over the system.

And for `.env`:

> Secrets belong in the environment, not in source. `.env` is a local
> dev convention; production injects the same names through the
> orchestrator. `.env.example` documents the contract.

Head to `examples/01_venv_inspect.py` for a runnable script that prints
the same information `construct.py` will print.
