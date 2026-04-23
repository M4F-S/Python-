# Course Upgrade Options

The course today is plain Markdown + runnable Python + a pytest suite.
That's solid for self-study, but several higher-value layers are cheap
to add. Pick based on what matters most: self-verification, guided
progression, social learning, or publication.

Ordered roughly by effort (lowest first).

---

## 1. Local verification — **partially done**

**What's there now.** `course/tests/test_all_solutions.py` runs every
reference solution (39 cases) and confirms each emits the canonical
lines the subject PDFs specify. ~2s end-to-end.

**Next step.** Fork the same idea for the `exercises/` starters: when
a student implements an exercise, `pytest tests/exercise/` tells them
whether it matches the spec without having to diff against
`solutions/`. This would be a per-exercise test file with the same
expectations as the solution test, but imports from `exercises/`
instead of `solutions/`.

Effort: half a day. Pure Python, stays in git.

---

## 2. Pre-commit lint/type pipeline

Add `.pre-commit-config.yaml` with:

- `flake8` (42's required linter),
- `mypy --strict` where feasible (all solutions should already pass),
- `end-of-file-fixer`, `trailing-whitespace`.

Plus a GitHub Actions workflow that runs `pytest + flake8 + mypy` on
every push. Catches regressions the moment they happen — more valuable
than any static documentation.

Effort: 1–2 hours.

---

## 3. `uv` or `poetry` lockfile

Right now `requirements.txt` says `pydantic>=2`. A lockfile (`uv.lock`
or `poetry.lock`) pins every transitive dependency and makes the
`make install` / CI reproducible. Module 08 already talks about the
pip-vs-Poetry split; treating the course itself as a Poetry project
would be an honest demonstration.

Effort: 30 minutes with `uv`.

---

## 4. Interactive CLI — `python3 -m course`

A thin click/typer front-end:

```
course status                   # which exercises you've finished
course start 05/ex1             # opens the lesson + starter in $EDITOR
course check 05/ex1             # runs the pytest expectations for that ex
course peek 05/ex1              # reveals the solution (writes a log line)
course stats                    # time-spent + tests-passing dashboard
```

A `progress.json` in the repo root tracks state; `course peek` bumps a
"times peeked" counter so honor-system violations are visible on review.

Effort: 1–2 days for a polished CLI.

---

## 5. Jupyter notebook variants of the lessons

Convert each `lesson.md` to a `.ipynb` with the runnable examples
inline. Students can `jupyter lab course/` and hit Shift-Enter through
the concepts. Code cells for the exercise starters, an empty cell for
their solution, a hidden test cell at the bottom.

`jupytext` can keep `.md` and `.ipynb` in sync, so git diffs stay
text-friendly.

Effort: half a day per module; can be automated with a small script.

---

## 6. GitHub Classroom / Autograder

Turn the pytest suite into a GitHub Classroom grader. A student forks
the repo, pushes their `exercises/` solutions, and a GH Actions job
runs the tests and comments the result on the PR. Works well for
cohort-based learning.

Effort: 1 day once the per-exercise tests exist (see #1).

---

## 7. Web front-end (static site)

Publish the lessons as a static site via **MkDocs** or **Quarto**:

- Every `lesson.md` becomes a page with a table of contents.
- A Python syntax-highlighted code block near each exercise, with a
  "copy as starter" button.
- `pyodide` embedded at the bottom of each lesson so students can run
  snippets in-browser without installing Python.

Effort: 1 day for a basic MkDocs site; 2–3 days with pyodide embeds.

---

## 8. Spaced-repetition flashcard set

Every lesson has a "Key concepts" table. Export those to Anki
(`*.apkg`) or Mochi. Works well alongside the hands-on exercises — the
flashcards cover the conceptual side (e.g., "what does `nonlocal` do?"),
the exercises cover the hands-on side.

Effort: half a day to write a Markdown-to-Anki converter.

---

## 9. Video walkthroughs

The `examples/` scripts are natural narrations. Screen-record yourself
running through each `examples/01_*.py`, committing to a short
(5–10 min) video per module. Publish as YouTube unlisted or host
locally.

Effort: ongoing, but ~30 min recording + 30 min editing per module.

---

## 10. Multi-language bridges

Because you come from C, a companion `c-to-python/` appendix could
show side-by-side equivalents for every concept: linked list in C vs.
`list` in Python, `struct` vs. `dataclass`, `fopen` vs. `open(...)`,
etc. Would make the course more marketable to other systems-programmers
moving to Python.

Effort: medium — 20–30 paired snippets.

---

## Recommended next moves

Given you've already got a working text course + 39 passing tests, the
two moves with the highest return on effort are:

1. **CI + pre-commit (option 2)** — enforces what's already true and
   immediately visible on GitHub.
2. **Per-exercise tests (option 1 expansion)** — turns the course into
   a true self-guided loop: write code, run `pytest`, see green, move
   on.

Both together: one weekend.

Then, depending on audience:

- If **you**: stop here and work through the exercises.
- If **cohort**: add option 6 (GitHub Classroom).
- If **public**: add option 7 (MkDocs site) then option 5 (notebooks).
