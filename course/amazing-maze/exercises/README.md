# Amazing Project — Exercise Workspace

This is the capstone. Build the full maze generator yourself. Target
structure:

```
exercises/
├── a_maze_ing.py        # CLI entry point
├── config.txt           # default config
├── pyproject.toml       # packaging
├── Makefile             # install/run/debug/clean/lint/lint-strict
├── README.md            # project-level README (subject has a minimum spec)
├── .gitignore
└── mazegen/             # reusable package (installable)
    ├── __init__.py
    └── generator.py
```

Milestones:

1. Write the `MazeGenerator` class. Use the randomised recursive
   backtracker. Add type hints and docstrings.
2. Implement `shortest_path()` (BFS) and `render_ascii()`.
3. Implement `encode_output()` matching the subject's hex format.
4. Wire up `a_maze_ing.py` with config parsing and graceful error
   handling (no unhandled exceptions reach the user).
5. Add the "42" stencil as a set of forbidden cells; gracefully skip it
   on small mazes with a stderr warning.
6. Build a wheel with `python3 -m build` and place
   `mazegen-1.0.0-py3-none-any.whl` at the project root.
7. Fill out `README.md` per the subject's required sections.

See the `../solutions/` folder for a full reference implementation; only
open it after your own version passes `make lint` and runs end-to-end.
