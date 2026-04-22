*This project has been created as part of the 42 curriculum by student.*

# A-Maze-ing

## Description

A configurable maze generator written in Python. Reads a plain-text
configuration file, generates a maze of `WIDTH` x `HEIGHT` cells (perfect
or with small loops), computes the shortest path between the configured
entry and exit, draws a "42" stencil in the middle using fully walled
cells, renders the result to the terminal, and writes a hex-encoded
output file following the subject's format.

The generation logic lives in a reusable package called `mazegen` that
can be installed with `pip` and imported into any other Python project.

## Instructions

```bash
make install            # installs the package editable + dev tools
make run                # runs with config.txt
python3 a_maze_ing.py my_config.txt
make lint               # flake8 + mypy (relaxed)
make lint-strict        # flake8 + mypy --strict
make build              # produces mazegen-1.0.0-*.whl + .tar.gz in dist/
make clean              # removes caches and generated artefacts
```

### Config file format

One `KEY=VALUE` per line. Lines starting with `#` are comments. Whitespace
around keys and values is ignored; keys are case-insensitive.

| Key           | Required | Example                | Notes                        |
|---------------|----------|------------------------|------------------------------|
| `WIDTH`       | Yes      | `WIDTH=25`             | Cells per row, >= 2          |
| `HEIGHT`      | Yes      | `HEIGHT=15`            | Cells per column, >= 2       |
| `ENTRY`       | Yes      | `ENTRY=0,0`            | `x,y` inside the grid        |
| `EXIT`        | Yes      | `EXIT=24,14`           | Distinct from ENTRY          |
| `OUTPUT_FILE` | Yes      | `OUTPUT_FILE=maze.txt` | Path to write the hex file   |
| `PERFECT`     | Yes      | `PERFECT=True`         | `True`/`False`/`yes`/`no`    |
| `SEED`        | No       | `SEED=42`              | Integer for reproducibility  |

Invalid / missing keys produce a clear error message.

### Output file layout

```
<row 0 hex digits>
...
<row height-1 hex digits>
<blank line>
<entry_x>,<entry_y>
<exit_x>,<exit_y>
<path as N/E/S/W letters>
```

Each hex digit encodes the four walls of a cell:

| Bit | Wall  |
|-----|-------|
| 0   | North |
| 1   | East  |
| 2   | South |
| 3   | West  |

`1` means the wall is closed; `0` means it is open. Coherence is
maintained across neighbours.

## Algorithm

The generator uses the **randomised recursive backtracker** (depth-first
search with random neighbour choice). Chosen because:

- It guarantees a perfect maze on its own (no post-processing required).
- Fast: O(WIDTH x HEIGHT) time and O(WIDTH x HEIGHT) stack space.
- Produces long winding corridors — visually more maze-like than
  Kruskal's or Prim's randomised variants.

For non-perfect mazes, after the DFS the generator randomly knocks down
~5% of the remaining interior walls, re-checking the "no 3x3 open area"
constraint and rolling back any opening that would violate it.

The "42" cells are marked as forbidden before generation starts; the
backtracker never enters them, so they stay walled on all four sides
and form the stencil when rendered. If the maze is too small to fit the
stencil, the program prints a warning and produces a plain maze.

## Reusable module (`mazegen`)

Install the module into another project:

```bash
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

Use it:

```python
from mazegen import MazeGenerator

gen = MazeGenerator(
    width=20,
    height=15,
    seed=42,
    perfect=True,
    forbidden={(5, 5), (5, 6)},   # optional
)
gen.generate()
grid = gen.cells                  # list[list[int]] of wall bitmasks
path = gen.shortest_path(entry=(0, 0), exit_=(19, 14))
ascii_art = gen.render_ascii(entry=(0, 0), exit_=(19, 14), path=path)
out = gen.encode_output(entry=(0, 0), exit_=(19, 14), path=path)
```

The package exports `MazeGenerator` and `MazeGenerationError`; every
other name is an implementation detail.

## Resources

- Jamis Buck, *Mazes for Programmers* — the canonical catalogue of
  maze-generation algorithms, including the recursive backtracker.
- [Think Labyrinth!](http://www.astrolog.org/labyrnth/algrithm.htm)
- Python docs: `collections.deque` (BFS), `random.Random` (seeded RNG),
  `typing` module (type hints), PEP 517 / 621 (pyproject.toml packaging).
- AI usage: I used Claude to help prototype the hex-encoding scheme and
  to sanity-check the "no open 3x3" invariant. All production code was
  written and reviewed by me.

## Team & process

Solo project for this scaffold; see the course's `README.md` for the
larger curriculum structure.

- Planning: algorithm selection → core `MazeGenerator` → output encoding
  → CLI wrapper → packaging → documentation.
- What went well: the reusable `mazegen` package fell out naturally from
  keeping generation logic out of the CLI.
- What could improve: the "42" stencil is a fixed bitmap; a more
  flexible glyph loader would let users draw other patterns.
- Tooling: `make`, `flake8`, `mypy`, `build`, plain `pip`.
