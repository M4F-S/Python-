# Module 02 — Garden Guardian: Exception Handling

> **Subject PDF:** `../../py-02.pdf`. Five exercises. Focus: `try`/`except`,
> `raise`, custom exception classes, and `finally`.

---

## 1. C error handling vs Python exceptions

In C you propagate errors via return codes or `errno`:

```c
int n = atoi(s);
if (n == 0 && s[0] != '0') { /* how do I even know it failed? */ }
FILE *f = fopen("x", "r");
if (!f) perror("fopen");
```

Python uses **exceptions**: error objects that unwind the call stack until
someone catches them.

```python
try:
    n = int(s)
except ValueError as e:
    print("parse failed:", e)
```

Benefits:
- You can't forget to check. If nobody catches the exception, the program
  dies with a traceback (good for bugs, bad for production).
- Error information travels with the exception object (`str(e)`, `e.args`).
- Separate the happy path from recovery visually.

---

## 2. The four keywords

```python
try:
    risky()                 # code that might fail
except ValueError as e:     # catch a specific exception
    handle(e)
except (KeyError, IOError): # catch multiple exception types
    handle_any()
except Exception:           # catch-all (use sparingly)
    handle_unknown()
else:
    # runs if no exception was raised in try
    ...
finally:
    # always runs, whether there was an exception or not
    cleanup()
```

### `raise`

```python
raise ValueError("temperature too low")   # create and raise
raise                                     # re-raise current exception
```

### Built-in exceptions you'll use in this module

| Exception | When |
|---|---|
| `ValueError` | `int("abc")`, bad argument value |
| `TypeError` | `"a" + 1`, wrong type |
| `ZeroDivisionError` | `1/0` |
| `FileNotFoundError` | `open("missing")` |
| `KeyError` | `d["missing"]` |
| `IndexError` | `lst[999]` |
| `AttributeError` | `obj.missing` |
| `Exception` | base class — catches every exception above |

---

## 3. Writing your own exceptions

```python
class GardenError(Exception):
    """Base class for all garden-related errors."""
    DEFAULT = "Unknown garden error"

    def __init__(self, message: str = "") -> None:
        super().__init__(message or self.DEFAULT)


class PlantError(GardenError):
    DEFAULT = "Unknown plant error"


class WaterError(GardenError):
    DEFAULT = "Unknown water error"
```

Key point — inheritance lets you **catch by category**:

```python
try:
    do_something()
except PlantError as e:       # specific
    ...
except GardenError as e:      # any garden error, including PlantError+WaterError
    ...
except Exception as e:        # everything else
    ...
```

Python checks `except` clauses top-to-bottom and uses the first matching one,
so put specific classes before their parents.

---

## 4. `finally` and clean-up

```python
def test_watering_system() -> None:
    print("Opening watering system")
    try:
        water_plant("Tomato")
        water_plant("lettuce")   # this will raise
        water_plant("Carrots")   # this never runs
    except PlantError as e:
        print(f"Caught PlantError: {e}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system")
```

Yes — `finally` runs **even when the function has already `return`ed**. It's
the one reliable spot to close files, release locks, etc.

> In Module 04 you'll meet `with open(...) as f:` which uses context
> managers to guarantee cleanup without `finally`. For now, use `finally`.

---

## 5. Type hints for functions that raise

`mypy` cares about input and output types; it does not verify exception
flow. Type hints on a function like `input_temperature` look like:

```python
def input_temperature(temp_str: str) -> int:
    ...
```

If your function might also accept a number (`int` or `str`), use a union:

```python
def input_temperature(temp_str: str | int) -> int:
    ...
```

(Python 3.10+ required for the `|` union syntax — which the PDF mandates.)

---

## 6. The exercises in two lines each

| # | File | Adds |
|---|---|---|
| 0 | `ft_first_exception.py` | Catch `ValueError` from `int("abc")`. |
| 1 | `ft_raise_exception.py` | Also `raise` when temperature is outside 0-40°C. |
| 2 | `ft_different_errors.py` | Demonstrate `ValueError`, `ZeroDivisionError`, `FileNotFoundError`, `TypeError` — catch each, then catch all in one `except`. |
| 3 | `ft_custom_errors.py` | Define `GardenError`, `PlantError`, `WaterError` (inheriting from `GardenError`). Show catching specific and by base class. |
| 4 | `ft_finally_block.py` | `water_plant(name)` raises `PlantError` if name isn't capitalized. `finally` closes the watering system. |

### Important rule from the PDF

> *Your programs must never crash.*

Every call that can raise must be wrapped. Your `main` block must never let
an exception escape unless the subject says so.

### `mypy` trap in ex2

The PDF warns you that `mypy` will complain about `"a" + 1` in the
`TypeError` case. That's intentional — the whole point of the exercise is
to trigger a TypeError at runtime. You can add `# type: ignore` on that
line to keep mypy quiet without changing the runtime behaviour.

---

## 7. Running

```bash
cd exercises/ex0 && python3 ft_first_exception.py
mypy ft_first_exception.py
flake8 ft_first_exception.py
```
