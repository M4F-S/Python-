"""Mirror lesson.md files into docs/modules/ for MkDocs.

MkDocs needs every page under docs_dir. Rather than duplicating
content, we symlink (on POSIX) or copy (on Windows) each lesson into
docs/modules/<slug>.md, and also sync the top-level README and
UPGRADES.md into docs/index.md etc.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


SRC_TO_DEST = [
    (ROOT / "README.md", DOCS / "index.md"),
    (ROOT / "UPGRADES.md", DOCS / "upgrades.md"),
    (ROOT / "c-to-python.md", DOCS / "c-to-python.md"),
]


def _sync(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() or dest.is_symlink():
        dest.unlink()
    # Use a copy so MkDocs sees real files on every platform, including
    # Windows where symlinks are unreliable.
    shutil.copyfile(src, dest)


def main() -> int:
    for src, dest in SRC_TO_DEST:
        if src.exists():
            _sync(src, dest)
            print(f"synced {src.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")
    modules_dir = DOCS / "modules"
    modules_dir.mkdir(parents=True, exist_ok=True)
    lessons = sorted(ROOT.glob("module-*/lesson.md")) + [ROOT / "amazing-maze/lesson.md"]
    for lesson in lessons:
        if not lesson.exists():
            continue
        slug = lesson.parent.name.replace("module-", "")
        dest = modules_dir / f"{slug}.md"
        _sync(lesson, dest)
        print(f"synced {lesson.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")
    # Setup + tests pages (small, written inline)
    (DOCS / "setup.md").write_text(SETUP_MD)
    (DOCS / "tests.md").write_text(TESTS_MD)
    print("wrote docs/setup.md, docs/tests.md")
    return 0


SETUP_MD = """# Setup

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
"""

TESTS_MD = """# Test harness

The course ships with two pytest suites.

## `tests/test_all_solutions.py`

Runs every **reference solution** in `solutions/` against the canonical
output lines published in each subject PDF. This suite is part of CI
and must stay green on every commit to `main`.

```bash
pytest tests/test_all_solutions.py -q
```

## `tests/exercises/`

Runs the same expectations against `exercises/` — the files cadets
fill in. Fresh starter stubs always fail; a correct implementation
turns each case green.

```bash
pytest tests/exercises -q                 # everything
pytest tests/exercises -k 05/ex1          # just one exercise
course check 05/ex1                       # same thing via the CLI
```

## Coverage map

| Suite                        | Tests | Purpose                                |
|------------------------------|------:|----------------------------------------|
| `test_all_solutions.py`      |    39 | Regression guard on reference code     |
| `tests/exercises/`           |    34 | Instant feedback loop for learners     |

CI runs both suites on push / PR via `.github/workflows/ci.yml` on
Python 3.10, 3.11, and 3.12.
"""


if __name__ == "__main__":
    raise SystemExit(main())
