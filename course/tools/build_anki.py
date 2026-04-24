"""Build an Anki flashcard deck covering the course's key concepts.

Usage:
    python -m tools.build_anki                 # writes dist/course.apkg

Requires `genanki` (installed via `pip install 42-python-rank2-course[anki]`).
If `genanki` isn't importable, the script falls back to writing a CSV
that Anki can import via File → Import.

The cards are pulled from a hand-curated dict (CARDS below) so the
deck stays focused on material that's actually in the course.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path


DIST = Path(__file__).resolve().parents[1] / "dist"
DECK_NAME = "42 Python Rank 2"


CARDS: list[tuple[str, str, str]] = [
    # (deck/subdeck tag, front, back)
    ("00-fundamentals", "How do you declare a variable with a type in Python?",
     "`name: int = 42`. Type hints are annotations; they don't affect runtime "
     "but are checked by mypy."),
    ("00-fundamentals", "What's the Python equivalent of C's `printf(\"%d\\n\", x)`?",
     "`print(x)` or `print(f\"{x}\")`. Python adds a newline by default."),
    ("00-fundamentals", "Can you define a function outside any class in Python?",
     "Yes. Python has top-level functions just like C. They become module-level "
     "names after the file is imported."),

    ("01-oop", "Explain `self` in a Python method.",
     "`self` is the instance passed as the first argument to every method call. "
     "Equivalent to the implicit `this` in C++/Java but named explicitly."),
    ("01-oop", "How does Python encapsulate attributes?",
     "By convention: a leading underscore (`self._height`) signals 'private'. "
     "There is no enforced `private` keyword."),
    ("01-oop", "Difference between `@staticmethod` and `@classmethod`.",
     "`@staticmethod` is a plain function inside a class (no implicit first "
     "argument). `@classmethod` receives the class (`cls`) as first argument "
     "and is typically used for alternate constructors."),

    ("02-errors", "How do you define a custom exception in Python?",
     "`class MyError(Exception): pass`. Subclass from `Exception` (or one of "
     "its subclasses) and raise it with `raise MyError('message')`."),
    ("02-errors", "What's the difference between `except Foo:` and `except Foo as e:`?",
     "`as e` binds the exception instance to a variable so you can inspect "
     "`e.args`, `str(e)`, etc. Without `as`, you just handle and move on."),
    ("02-errors", "When does `finally` run?",
     "Always — on normal exit, on exceptions, and even on `return`/`break` "
     "from inside the try. Use it for cleanup (closing files, releasing locks)."),

    ("03-collections", "list vs. tuple — when to use which?",
     "`list` is mutable and grows; `tuple` is immutable and hashable (so it "
     "can be a dict key). Use tuple for fixed-length records, list for homogeneous "
     "sequences that change."),
    ("03-collections", "What's a generator?",
     "A function that uses `yield` instead of `return`. It produces values "
     "lazily; iteration pauses and resumes at each yield point."),
    ("03-collections", "List comprehension syntax?",
     "`[f(x) for x in xs if cond(x)]`. Same for sets (`{...}`) and dicts "
     "(`{k: v for k, v in ...}`)."),

    ("04-fileio", "What does `with open(...) as f:` do?",
     "Opens the file, binds the handle to `f`, and guarantees `f.close()` is "
     "called when the block exits — even on exception. Context manager pattern."),
    ("04-fileio", "How to write to stderr in Python?",
     "`print('msg', file=sys.stderr)` or `sys.stderr.write('msg\\n')`."),

    ("05-polymorphism", "What does `@abstractmethod` do?",
     "Marks a method required on every concrete subclass. Instantiating a class "
     "that doesn't override all abstract methods raises `TypeError`. Needs the "
     "class to inherit from `abc.ABC`."),
    ("05-polymorphism", "What's a `typing.Protocol`?",
     "A structural-subtyping interface: any object that has the right method "
     "shape satisfies it, without explicit inheritance. Like Go interfaces."),

    ("06-imports", "Absolute vs. relative import — example of each.",
     "Absolute: `from alchemy.potions import strength_potion`. Relative: "
     "`from .potions import strength_potion` (same package). Relative uses dots."),
    ("06-imports", "What's `__init__.py` for?",
     "Marks a directory as a package and runs its body when the package is "
     "first imported. Typical use: re-export public names from submodules."),
    ("06-imports", "How do you break a circular import?",
     "Three options: (1) import inside the function that needs the name, "
     "(2) pass the dependency as an argument, (3) extract the shared code "
     "into a third module neither party owns."),

    ("07-abstract", "Describe the abstract-factory pattern in one sentence.",
     "A factory class returns instances of an abstract product type so "
     "callers never name the concrete class directly."),
    ("07-abstract", "Mixin / capability class — what problem does it solve?",
     "Lets you bolt orthogonal behaviour (e.g. 'can heal') onto unrelated "
     "classes via multiple inheritance, without deepening any single hierarchy."),

    ("08-matrix", "How do you detect inside Python whether you're in a venv?",
     "`sys.prefix != sys.base_prefix`. The two diverge only inside an active "
     "virtual environment."),
    ("08-matrix", "What is a `.env` file and why is it gitignored?",
     "A local file with `KEY=VALUE` pairs the app reads at startup (via "
     "`python-dotenv` or similar). It holds secrets and must never be committed."),
    ("08-matrix", "Difference between `requirements.txt` and `pyproject.toml`.",
     "requirements.txt is a flat list of installs for `pip install -r`. "
     "pyproject.toml (PEP 517/518/621) declares project metadata, build "
     "backend, and dependencies — the modern standard."),

    ("09-pydantic", "What does `@model_validator(mode='after')` do?",
     "Runs after per-field validation, on the fully parsed model. Use it to "
     "enforce rules that span multiple fields. Must return `self`."),
    ("09-pydantic", "How do you configure a min/max on a numeric Pydantic field?",
     "`Field(ge=0, le=100)` for inclusive bounds; `gt`/`lt` for exclusive."),
    ("09-pydantic", "How does Pydantic map a string like '2024-01-01T00:00:00' to datetime?",
     "Pydantic v2 coerces common ISO-8601 strings into `datetime` automatically "
     "when the field is typed as `datetime`. Use `model_config=ConfigDict(strict=True)` "
     "to disable coercion."),

    ("10-functional", "When is a `lambda` the right choice?",
     "For a *single-expression* function you only use once, usually as an "
     "argument to `sorted(key=...)`, `map`, `filter`. If you'd name it or "
     "test it, write `def` instead."),
    ("10-functional", "Explain a closure in two sentences.",
     "A function plus the non-local variables it references. Python captures "
     "them automatically when the function is defined, and `nonlocal` lets "
     "you assign to them."),
    ("10-functional", "What does `@functools.wraps` do?",
     "Inside a decorator, copies `__name__`, `__doc__`, `__wrapped__` from "
     "the wrapped function onto the wrapper so introspection (help, pytest, "
     "debuggers) shows the right metadata."),
    ("10-functional", "Why is `global` forbidden in module 10 but `nonlocal` allowed?",
     "`global` couples functions to module-wide mutable state — anti-pattern. "
     "`nonlocal` binds a name to an enclosing *function* scope, which is "
     "exactly how closures communicate. Functional style favours the second."),

    ("amazing-maze", "Describe the randomised recursive backtracker in two sentences.",
     "DFS from a start cell; at each step, knock down the wall to a random "
     "unvisited neighbour and recurse. On dead-end, pop the stack — the "
     "tree-like carving is a perfect maze."),
    ("amazing-maze", "Why is BFS the right algorithm for the shortest path on the maze grid?",
     "All edges have uniform cost (1 step), so breadth-first traversal finds "
     "the minimum-step path in O(V+E) without needing a priority queue."),
]


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["deck", "front", "back"])
        for tag, front, back in CARDS:
            writer.writerow([f"{DECK_NAME}::{tag}", front, back])


def write_apkg(path: Path) -> bool:
    try:
        import genanki  # type: ignore
    except ImportError:
        return False

    model = genanki.Model(
        1735189201,
        "42 Python Rank 2 Basic",
        fields=[
            {"name": "Front"},
            {"name": "Back"},
            {"name": "Subdeck"},
        ],
        templates=[
            {
                "name": "Card",
                "qfmt": "<div style='font-size:18px'>{{Front}}</div>",
                "afmt": (
                    "{{FrontSide}}<hr>"
                    "<div style='font-size:16px'>{{Back}}</div>"
                    "<br><small>{{Subdeck}}</small>"
                ),
            }
        ],
    )

    decks_by_tag: dict[str, genanki.Deck] = {}
    for tag, front, back in CARDS:
        full = f"{DECK_NAME}::{tag}"
        deck = decks_by_tag.setdefault(
            full,
            genanki.Deck(abs(hash(full)) % (10**10), full),
        )
        deck.add_note(
            genanki.Note(
                model=model,
                fields=[front, back, tag],
                tags=[tag],
            )
        )

    package = genanki.Package(list(decks_by_tag.values()))
    path.parent.mkdir(parents=True, exist_ok=True)
    package.write_to_file(str(path))
    return True


def main() -> int:
    apkg = DIST / "course.apkg"
    csv_path = DIST / "course.csv"
    if write_apkg(apkg):
        print(f"wrote {apkg.relative_to(Path.cwd())} ({len(CARDS)} cards)")
    else:
        print(
            "genanki not available - falling back to CSV. "
            "Install with: pip install 'genanki>=0.13'",
            file=sys.stderr,
        )
    write_csv(csv_path)
    print(f"wrote {csv_path.relative_to(Path.cwd())} ({len(CARDS)} cards)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
