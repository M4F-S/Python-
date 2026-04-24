# Running this course as a GitHub Classroom assignment

This repo doubles as a GitHub Classroom template. Instructors clone
once, tweak the README, and distribute forks to a cohort; students
push to `student/*` or `submission/*` branches and the autograder runs
on every push.

## Setup (instructor, one-time)

1. Create a GitHub Classroom assignment linked to this repository.
2. In the classroom settings, pick **Individual assignment** and point
   the grading workflow at `.github/workflows/classroom.yml`.
3. Optionally enable a deadline; the workflow's exit code is what
   Classroom reads for the grade.

## What the grader runs

`pytest tests/exercises/` — the same 34 parametrised cases a cadet
sees locally via `course check`. The suite asserts that every
exercise prints the canonical lines the subject PDF specifies, using
subprocess runs for most modules and `importlib` for Module 00 (whose
subject forbids `if __name__ == "__main__":`).

A JUnit XML report is produced and converted to a Markdown summary
that appears in the workflow run's **Summary** tab via
`tools/summarise_junit.py`.

## What students see

On every push to a `student/**` or `submission/**` branch:

1. CI installs dependencies, runs the full exercise suite.
2. The step summary shows a table: passed / failed / skipped per
   suite, plus a collapsed list of failing test names.
3. Test results are attached to the commit as a check.

Students can reproduce the grade locally:

```bash
pytest tests/exercises -q
# or
course check                  # same thing via the CLI
```

## Adapting to your campus

- Renaming the target branch: edit the `on.push.branches` list in
  `.github/workflows/classroom.yml`.
- Adding private tests: put them under `course/tests/private/` and
  extend the grader command. Keep the file out of any fork that
  reaches students.
- Tightening the threshold: replace `continue-on-error: true` on the
  grader with a `--tb=short --maxfail=1` to fail-fast, or use `pytest
  --junitxml + check-file-coverage` style gates.

## Honor-system reminder for cadets

`solutions/` is right there in the repo. The `course peek` CLI
records every look in `.course-progress.json`. Peer reviewers can
(and will) scroll through that file before they grade the defence —
so leaning on it shows up.
