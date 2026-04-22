# Amazing Project — A-Maze-ing

> *"A labyrinth is not a place to be lost, but a path to be found."*

The capstone ties every previous module together into one program:

| Module                 | Used in                                                    |
|------------------------|------------------------------------------------------------|
| 00 Fundamentals        | Grid arithmetic, CLI args.                                 |
| 01 OOP                 | `MazeGenerator`, `Cell`, `Renderer` classes.               |
| 02 Errors              | `MazeConfigError`, `MazeGenerationError`.                  |
| 03 Collections         | `set` of visited cells, `deque` BFS, dict for config.      |
| 04 File I/O            | Reading `config.txt`, writing the hex output.              |
| 05 Polymorphism        | Swap a `Renderer` via Protocol.                            |
| 06 Imports             | The `mazegen` package is an importable module.             |
| 07 Abstract Classes    | Abstract `Algorithm` + `RecursiveBacktracker` subclass.    |
| 08 Venvs & Packaging   | `pyproject.toml`, Makefile, build a wheel.                 |
| 09 Pydantic            | Validated `MazeConfig` model.                              |
| 10 Functional          | `@lru_cache` on hot paths, decorators, closures.           |

Not every tool appears in every file — each shows up where it's natural.

## Problem overview

You are given a textual config file. You must:

1. Parse it (with validation) into a `MazeConfig`.
2. Generate a maze of `WIDTH × HEIGHT` cells with a random-but-seedable
   algorithm.
3. Ensure entrance and exit exist, the graph is connected (aside from
   the "42" pattern), no 3×3 open area exists, and (if `PERFECT=True`)
   there is exactly one path between entry and exit.
4. Compute a shortest path from entry to exit.
5. Write an output file: hex grid, blank line, entry, exit, path.
6. Render a visual representation with the solution path overlaid.
7. Ship all of this as a pip-installable package named `mazegen-*`.

## Cell encoding

Each cell is a 4-bit bitmask of *closed* walls:

| Bit | Direction |
|-----|-----------|
| 0   | N         |
| 1   | E         |
| 2   | S         |
| 3   | W         |

- `0xF` = 1111 = all four walls.
- `0x3` = 0011 = N + E walls closed, S + W open.
- `0x0` = no walls (open on every side).

A coherent grid means: if cell `(x, y)` has its east wall closed, then
`(x+1, y)` has its west wall closed. Build one `carve(a, b)` helper that
opens *both* sides at once and you never violate that.

## Algorithm: randomised recursive backtracker (DFS)

Simplest algorithm that guarantees a *perfect* maze (one path between
any two cells).

```
stack = [start]
visited = {start}
while stack:
    cell = stack[-1]
    unvisited_neighbours = [n for n in neighbours(cell) if n not in visited]
    if not unvisited_neighbours:
        stack.pop()
        continue
    next_cell = random.choice(unvisited_neighbours)
    carve(cell, next_cell)      # opens wall between them
    visited.add(next_cell)
    stack.append(next_cell)
```

Complexity: O(width × height). Seed `random.Random(seed)` for reproducible
output.

For a non-perfect maze: run the backtracker, then randomly knock down a
small fraction (~5%) of the remaining interior walls. Check each removal
against the "no 3×3 open area" constraint and skip it if it would
violate the rule.

## BFS for the solution path

Shortest path on an unweighted grid = BFS. `collections.deque` gives you
O(1) popleft. Build a parent map as you go, then walk backwards from the
exit to the entry to recover the path, emitting `N`/`E`/`S`/`W` as you
move.

## The "42" pattern

A 3-row × 7-column bitmap drawn with fully walled cells. Positioned in
the middle of the maze if it fits (height >= 3 and width >= 8 or so).
Mark the cells as "forbidden" before generation; the backtracker never
enters them, so they stay isolated. Good choice of bitmap:

```
11111 1111     ->    "42" stencil, each X = all-walls cell
11  1 1  1
1111  1111
1  1     1
1  1     1
```

(Exact shape is up to you — "42" in *any* readable bitmap passes
evaluation.)

## Packaging (`mazegen-*`)

`pyproject.toml` + `setuptools` is enough. After `pip install build`:

```
python3 -m build
# ->  dist/mazegen-1.0.0.tar.gz
# ->  dist/mazegen-1.0.0-py3-none-any.whl
```

Put the wheel at the repo root (as the subject requires) and keep the
source in `mazegen/` next to it.

Importers use it like this:

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42, perfect=True)
gen.generate()
path = gen.shortest_path(entry=(0, 0), exit=(19, 14))
print(gen.render_ascii(path=path))
```

## Makefile targets

| Target          | What it runs                                                |
|-----------------|-------------------------------------------------------------|
| `install`       | `pip install -e .` + dev tooling                            |
| `run`           | `python3 a_maze_ing.py config.txt`                          |
| `debug`         | `python3 -m pdb a_maze_ing.py config.txt`                   |
| `clean`         | Delete `__pycache__/`, `.mypy_cache/`, `dist/`, `build/`.   |
| `lint`          | `flake8 .` + the mypy flags from the subject                |
| `lint-strict`   | `flake8 .` + `mypy . --strict`                              |

## README pointers

The root `README.md` must include:
- Italic first line crediting the curriculum.
- Description + Instructions + Resources sections.
- Config-file format description.
- Which algorithm you used + why.
- Which part of your code is reusable + how.
- Team roles / planning / retrospective.

See the reference README in `solutions/README.md`.

This module intentionally has **no auto-graded exact output** — the PDF
shows terminal screenshots but the text can vary. Aim for: correct hex
grid, one valid shortest path, visible "42" in the render, and the
`mazegen` wheel importable cleanly from another project.
