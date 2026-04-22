# Module 06 — Imports (The Codex)

> *"How do four separate files become one coherent program?"*

Python's import system is the single most surprising thing for C/C++ programmers.
There is no linker, no header files, no `#include`. Instead, **every module is
an object**, loaded lazily, cached in a dictionary (`sys.modules`), with
attributes populated by running the module top-to-bottom once.

Once you internalise that model, every weird behaviour (circular imports,
"why is my name not there yet?", `__init__.py` magic) becomes obvious.

## The four mysteries

### 1. Modules, packages, and `__init__.py`

- A **module** is a single `.py` file. Importing it runs every top-level
  statement once; anything assigned at the top level becomes an attribute on
  the module object.
- A **package** is a directory containing `__init__.py`. Importing the
  package runs `__init__.py`, which typically re-exports names from the
  package's submodules. The file itself becomes the package's module body.
- Since Python 3.3, packages without `__init__.py` also work (they are
  "namespace packages"), but 42 wants you to write a real `__init__.py`.

```
laboratory/
├── __init__.py          # code here is `laboratory` itself
├── elements.py          # laboratory.elements
└── potions/
    ├── __init__.py      # laboratory.potions
    └── recipes.py       # laboratory.potions.recipes
```

### 2. Import pathways (five shapes to recognise)

```python
import elements                                # A — module
from elements import create_fire               # B — name from module
import alchemy.elements                        # C — submodule
from alchemy.elements import create_air        # D — name from submodule
import alchemy                                 # E — package (runs __init__.py)
```

- `(A)` binds `elements` in your namespace; access as `elements.create_fire()`.
- `(B)` binds only `create_fire`.
- `(C)` makes `alchemy.elements` available; you still call via the full path
  `alchemy.elements.create_air()`.
- `(D)` binds just the function.
- `(E)` loads the package; you can only reach what `__init__.py` exposes.

### 3. Absolute vs relative imports

Inside a package, you can refer to sibling modules two ways:

```python
# absolute — uses the full dotted path from sys.path roots
from alchemy.potions import strength_potion

# relative — dots count steps up the package tree
from .potions import strength_potion     # same package
from ..elements import create_fire       # parent package
```

- Absolute imports are clearest for readers; prefer them by default.
- Relative imports are handy for moving/renaming packages without rewriting
  dozens of files.
- PEP 8 says: "explicit relative imports are an acceptable alternative to
  absolute imports, especially when dealing with complex package layouts."

### 4. Circular imports

`from a import x` evaluates `a` first. If `a` at some point does
`from b import y`, and `b` does `from a import z`, then when `b` runs, `a` is
only partially initialised and `z` may not be defined yet. You get:

```
ImportError: cannot import name 'z' from partially initialized module 'a'
(most likely due to a circular import)
```

Three clean ways to break the cycle:

1. **Import inside the function, not at the top.** By the time the function
   runs, all modules are fully initialised.
2. **Pass the data as an argument.** `validate(ingredients, allowed)` doesn't
   need to import anything.
3. **Refactor.** Move shared names into a third module both sides depend on.

In this project, Part IV makes you show both a working light-magic system
(no cycle) and a broken dark-magic system (cycle → explosion).

## C → Python crib sheet

| C/C++                                         | Python                                |
|-----------------------------------------------|---------------------------------------|
| `#include "math.h"`                           | `import math`                         |
| `extern int x;` then linking .o files         | Import the name: `from m import x`   |
| One `main()` per program                      | `if __name__ == "__main__":` guard    |
| Header/source split                           | Not needed — module is both           |
| Include guards (`#ifndef FOO_H`)              | Automatic — modules cached in `sys.modules` |
| Global initialisation order fiasco            | Python runs top-level code once in import order |

## `if __name__ == "__main__":`

When you `import foo`, `foo.__name__ == "foo"`. When you run
`python3 foo.py`, `foo.__name__ == "__main__"`. That's how a file detects
whether it's being executed directly or merely imported, and it's why you
tuck test code inside that guard.

## What `__init__.py` typically looks like

```python
"""Public API of the `alchemy` package."""
from .elements import create_air              # re-export (no create_earth!)
from .potions import strength_potion
from .potions import healing_potion as heal   # alias
from .transmutation.recipes import lead_to_gold
```

`from X import Y` inside `__init__.py` makes `Y` an attribute of the package,
so callers can write `alchemy.heal()` even though `heal` lives in
`alchemy/potions.py`. Anything you *don't* re-export is still reachable via
its full path (`alchemy.grimoire.dark_spellbook.dark_spell_record`) but not
on the package object itself — which is exactly the hiding behaviour
Exercise `ft_alembic_4` wants for `create_earth`.

> A blank `__init__.py` still makes the folder a package. Use that when you
> don't want to re-export anything.

## Flake8 and mypy quirks with `__init__.py`

- flake8 often complains about "unused import" in `__init__.py` files that
  re-export names. The standard fix is `__all__ = [...]` listing the
  re-exports (silences both flake8 and mypy's "implicit re-export" warning),
  or `# noqa: F401` next to the line.
- mypy wants `from X import Y as Y` (redundant alias) to treat the name as
  publicly re-exported. `__all__` has the same effect.

## Running scripts from the project root

42 expects you to run tests from the repo root:

```
$ python3 ft_alembic_2.py
```

When you invoke a script this way, **the directory containing the script is
added to `sys.path`**. That's why `import alchemy` works — `alchemy/` sits
in the same directory — and why `from elements import create_fire` works
inside `alchemy/potions.py` too, as long as you run from the root.

> It is forbidden (by the subject) to modify `sys.path`. Structure your tree
> so you don't need to.

Head over to `examples/01_import_tour.py` for a runnable walkthrough of
each of the five import shapes.
