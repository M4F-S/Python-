# 42 Berlin — Python Rank 2 Course

An open, self-paced course for cadets working through the Rank 2 Python
track at 42 Berlin (and any other 42 campus where the Python projects
`py-00` through `py-10` and `Amazing` are part of the curriculum). It's
grounded in the real subject PDFs — each one is shipped inside its
module folder as `subject.pdf`.

> **Coming from C?** 42 cadets reach Rank 2 with C mostly under their
> belts. Every lesson in this course explicitly maps concepts back to
> C (memory, typing, indentation, duck typing, OOP, imports vs.
> `#include`, etc.) so the mental model transfer is cheap.

## How the course is organized

```
course/
├── README.md                ← this file
├── UPGRADES.md              ← optional enhancements to the course itself
├── c-to-python.md           ← side-by-side C↔Python translation appendix
├── requirements.txt         ← shared dependencies (pydantic, pytest, ...)
├── pyproject.toml           ← course as a packaged project (uv/pip/poetry)
├── .pre-commit-config.yaml  ← lint + type + pytest hooks
├── mkdocs.yml               ← static-site generator config
├── course_cli/              ← installable `course` command
├── tools/                   ← anki export, jupyter converter, etc.
├── tests/                   ← pytest suite for every reference solution
├── docs/                    ← MkDocs site source (lessons mirrored)
├── notebooks/               ← Jupyter notebook variants of the lessons
├── module-00-fundamentals/
│   ├── subject.pdf          ← the original 42 subject PDF
│   ├── lesson.md            ← concepts + C→Python mapping
│   ├── examples/            ← tiny runnable demos
│   ├── exercises/           ← starter files cadets fill in (42 names)
│   └── solutions/           ← reference solutions (don't peek early)
├── module-01-oop/           ← same structure
├── module-02-errors/
├── module-03-collections/
├── module-04-fileio/
├── module-05-polymorphism/
├── module-06-imports/
├── module-07-abstract/
├── module-08-matrix/
├── module-09-pydantic/
├── module-10-functional/
└── amazing-maze/            ← capstone (mazegen wheel + a_maze_ing.py)
```

## The honor-system solutions policy

Reference solutions live in `solutions/`. The intended flow is simple:
cadets write their own answer in `exercises/` first, then only open
`solutions/` **after** submitting the work for peer review. Peeking early
means giving up the learning — and risks a plagiarism flag.

The `course peek` CLI command reveals a solution but records the event
in `.course-progress.json`, so peer reviewers can spot shortcuts.

## Setup (once)

### With `uv` (recommended — fastest, lockfile-based)

```bash
cd course
uv sync                      # reads pyproject.toml + uv.lock
source .venv/bin/activate
```

### With plain `pip`

```bash
cd course
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .             # installs the `course` CLI
```

### With `poetry`

```bash
cd course
poetry install
poetry shell
```

Verify:

```bash
python --version             # 3.10+ required
python -c "import pydantic; print(pydantic.VERSION)"
course status                # should list every module
```

## Working on a module

The intended loop per exercise:

```bash
course start 05/ex1          # opens lesson.md + the starter in $EDITOR
# ... implement in exercises/ ...
course check 05/ex1          # runs the exercise-specific pytest expectations
```

If the tests pass, move on. If a cadet is stuck after real effort,
`course peek 05/ex1` shows the reference solution and bumps a
peek-counter (honor system).

Fallback manual flow (no CLI needed):

```bash
cd module-05-polymorphism
cat lesson.md                # read top-to-bottom
ls examples/                 # tinker with the runnable tour
ls exercises/                # fill in each starter file
pytest tests/ -k 05/ex1      # verify against the subject's expectations
```

Every file name in `exercises/` and every function signature matches
the 42 subject PDF exactly, so cadets can submit straight from there.

## The roadmap

| #  | Module | Subject | Core skills |
|----|--------|---------|-------------|
| 00 | Fundamentals (Growing Code)         | `module-00-fundamentals/subject.pdf`  | variables, functions, control flow, type hints |
| 01 | OOP (Code Cultivation)              | `module-01-oop/subject.pdf`           | classes, inheritance, factory, encapsulation |
| 02 | Error handling (Garden Guardian)    | `module-02-errors/subject.pdf`        | try/except, custom errors, finally |
| 03 | Collections (Data Quest)            | `module-03-collections/subject.pdf`   | list/dict/set/tuple, comprehensions, generators |
| 04 | File I/O (Data Archivist)           | `module-04-fileio/subject.pdf`        | open/read/write, streams, context managers |
| 05 | Polymorphism (Code Nexus)           | `module-05-polymorphism/subject.pdf`  | abstract classes, method overriding, pipelines |
| 06 | Imports (The Codex)                 | `module-06-imports/subject.pdf`       | packages, `__init__.py`, relative vs absolute |
| 07 | Abstract architectures (DataDeck)   | `module-07-abstract/subject.pdf`      | ABCs, mixins, strategy pattern, factories |
| 08 | Virtualenvs & packaging (The Matrix)| `module-08-matrix/subject.pdf`        | `venv`, `pip`, `pyproject.toml`, `.env` |
| 09 | Pydantic (Cosmic Data)              | `module-09-pydantic/subject.pdf`      | BaseModel, Field, model_validator, nesting |
| 10 | Functional programming (FuncMage)   | `module-10-functional/subject.pdf`    | lambda, HOF, closures, functools, decorators |
| ★  | Amazing — maze generator            | `amazing-maze/subject.pdf`            | capstone: ships a pip-installable wheel |

## Running the test suite

Every reference solution is continuously verified:

```bash
pytest tests/                # 39+ solution tests, ~2-3s
pytest tests/exercises/      # per-exercise "did my answer work?" tests
```

The suite uses subprocesses for self-executing scripts, `importlib` for
Module 00 (where the 42 subject forbids `if __name__ == "__main__":`
blocks), and checks every canonical stdout line specified in the PDFs.

CI runs the same suite on every push via `.github/workflows/ci.yml`,
plus `flake8` and `mypy`. Local pre-commit hooks catch style issues
before they hit the remote.

## Other course surfaces

Cadets who prefer a different reading medium have options beyond raw
Markdown in a git repo:

| Surface               | How to use                                            |
|-----------------------|-------------------------------------------------------|
| **MkDocs site**       | `mkdocs serve` (http://localhost:8000)                |
| **Jupyter notebooks** | `jupyter lab notebooks/` — lessons as `.ipynb`        |
| **Anki flashcards**   | `python -m tools.build_anki` → `dist/course.apkg`     |
| **CLI workflow**      | `course start|check|peek|status` (see above)          |
| **PDFs**              | `<module>/subject.pdf` — the original 42 briefings    |

See `UPGRADES.md` for the roadmap of course improvements and which
ones are already live.

## Submission rules (important!)

42 grading is strict. Before turning in:

1. **Exact file names.** `exercises/` already uses the names the PDFs
   require — don't rename them.
2. **Forbidden imports.** Each subject PDF lists authorised modules.
   Importing anything else fails the moulinette.
3. **No blind copy-paste from AI or from `solutions/`.** Cadets have to
   explain every line in the peer review. The 42 honor code is explicit
   about this.
4. **Peer review.** Be ready to defend every line verbally, demonstrate
   the program with different inputs, and answer "what if we changed X?"
   questions.

## Contributing

Spotted a bug, an unclear lesson, or a missing edge case? PRs welcome.
CI enforces `flake8`, `mypy`, and the test suite — green CI required
before merge.

Good luck, cadet — and remember: the point of the journey is not the
certificate, it's the code you wrote to get it.
