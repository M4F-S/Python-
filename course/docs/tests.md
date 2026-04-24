# Test harness

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
