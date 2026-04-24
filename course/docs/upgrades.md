# Course Upgrades — Roadmap & Status

The course started life as plain Markdown + runnable Python + a pytest
suite. Each of the options below layered something on top: faster
feedback, better reading surfaces, or easier cohort-scale grading.

Status key: **✅ shipped**, **🟡 partially shipped**, **⬜ planned**.

---

## 1. ✅ Per-exercise self-verification

`tests/exercises/` parametrises the same canonical-output expectations
from `tests/test_all_solutions.py` but runs them against `exercises/`
— the files cadets actually fill in. Starter stubs fail (loudly, with
the missing string reported); a correct implementation turns each case
green.

Run everything:

```bash
pytest tests/exercises -q
```

Run a single exercise:

```bash
pytest tests/exercises -k 05/ex1
course check 05/ex1           # same thing through the CLI
```

Scope: 34 tests across modules 00–10.

---

## 2. ✅ Pre-commit + GitHub Actions CI

- `.pre-commit-config.yaml` wires up `flake8`, `mypy`, trailing-whitespace
  and merge-conflict hooks, plus an on-push `pytest` via `pre-push`
  stage.
- `.github/workflows/ci.yml` runs the full solution suite against Python
  3.10 / 3.11 / 3.12, lints, type-checks, and builds the
  `mazegen-*.whl` artefact.
- `.github/workflows/classroom.yml` runs the **exercise** suite on
  student branches and publishes a Markdown summary (see upgrade #6).

Install hooks once:

```bash
pre-commit install
pre-commit install --hook-type pre-push
```

---

## 3. ✅ `uv` lockfile

`pyproject.toml` declares the course as an installable project; `uv
sync` produces a resolved `uv.lock` so every machine pulls identical
versions. Plain `pip` and `poetry` flows still work — see
[Setup](./setup.md).

---

## 4. ✅ Interactive course CLI

`course_cli/` installs as a console script via `pyproject.toml`:

```bash
course list                  # every module + exercise
course status                # progress bar, per-exercise status
course start 05/ex1          # opens lesson + starter in $EDITOR
course check 05/ex1          # runs exercise pytest cases
course diff 05/ex1           # unified diff exercises/ vs solutions/
course peek 05/ex1 --reason "stuck on Protocol"
course reset 05/ex1          # git checkout -- exercises/05/ex1
```

Progress lives in `.course-progress.json` at the course root. `peek`
increments a counter so peer reviewers can see whether a cadet leaned
on the reference answer.

---

## 5. ✅ Jupyter notebook variants

`tools/md_to_ipynb.py` converts every `lesson.md` into a parallel
`.ipynb` under `notebooks/`. Each fenced `python` block becomes an
executable cell; the rest is Markdown. Re-run whenever a lesson
changes:

```bash
python -m tools.md_to_ipynb
jupyter lab notebooks/
```

---

## 6. ✅ GitHub Classroom autograder

`.github/workflows/classroom.yml` triggers on `student/**` and
`submission/**` branches, runs `pytest tests/exercises/`, and uses
`tools/summarise_junit.py` to post a Markdown summary to the workflow
step summary. Pair it with a GitHub Classroom assignment template that
points at this repo for cohort grading.

---

## 7. ✅ Static MkDocs site

`mkdocs.yml` + `tools/sync_docs.py` produce a browsable site under
`site/` combining:

- The README as the landing page.
- Every `lesson.md` as a navigable module page.
- Setup, Test harness, Upgrades, and the C→Python appendix as
  top-level entries.

```bash
python -m tools.sync_docs    # mirror Markdown into docs/
mkdocs serve                 # live preview at http://localhost:8000
mkdocs build                 # static HTML under site/
```

Deploying it to GitHub Pages is a single workflow step
(`mkdocs gh-deploy`); not enabled by default.

---

## 8. ✅ Anki flashcard export

`tools/build_anki.py` emits both a `.apkg` (native Anki import,
requires `genanki`) and a `.csv` (universal fallback) under `dist/`.
33 hand-curated cards cover one concept per sub-topic across every
module.

```bash
pip install "42-python-rank2-course[anki]"
python -m tools.build_anki
# -> dist/course.apkg  (double-click to import into Anki)
```

---

## 9. ⬜ Video walkthroughs

Record each `examples/01_*.py` being run and explained, one short
video per module. This requires human narration and screen recording,
so it's outside the scope of what the scaffold can generate. Tools to
use when you do record: OBS Studio, `asciinema` for terminal-only
segments, and `ffmpeg` for post-processing.

---

## 10. ✅ C → Python appendix

`c-to-python.md` (linked from the main README and the MkDocs nav) is a
side-by-side cheat sheet covering compilation model, primitive types,
memory management, arrays/strings, OOP, control flow, pointers,
error handling, containers, callbacks, formatting, and build tooling.

---

## What's left

Only #9 (video recording). Everything else has a working
implementation in-tree with CI coverage. Pick up recording if and when
a cadet cohort asks for it.
