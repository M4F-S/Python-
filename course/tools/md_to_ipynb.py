"""Convert every lesson.md into a matching .ipynb under notebooks/.

Run with:
    python -m tools.md_to_ipynb

Logic: every Markdown section is a Markdown cell; every fenced
```python block becomes an executable code cell so cadets can hit
Shift-Enter to run the example inline. Re-running the script is
idempotent - existing notebooks are overwritten.
"""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks"


def _make_cell(cell_type: str, source: str) -> dict:
    lines = source.splitlines(keepends=True)
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": lines,
        **(
            {"execution_count": None, "outputs": []}
            if cell_type == "code"
            else {}
        ),
    }


def md_to_cells(md: str) -> list[dict]:
    cells: list[dict] = []
    buf: list[str] = []
    in_code = False
    code_buf: list[str] = []

    def flush_md() -> None:
        if buf:
            text = "".join(buf).strip("\n")
            if text:
                cells.append(_make_cell("markdown", text + "\n"))
            buf.clear()

    for raw_line in md.splitlines(keepends=True):
        if raw_line.startswith("```python"):
            flush_md()
            in_code = True
            code_buf = []
            continue
        if in_code and raw_line.startswith("```"):
            in_code = False
            cells.append(_make_cell("code", "".join(code_buf).rstrip() + "\n"))
            code_buf = []
            continue
        if in_code:
            code_buf.append(raw_line)
        else:
            buf.append(raw_line)

    if in_code and code_buf:
        # unterminated ``` fence - treat remaining as markdown.
        cells.append(_make_cell("markdown", "```python\n" + "".join(code_buf)))
    flush_md()
    return cells


def convert(md_path: Path, out_path: Path) -> None:
    cells = md_to_cells(md_path.read_text())
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(notebook, indent=1) + "\n")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    lessons = sorted(ROOT.glob("module-*/lesson.md")) + [ROOT / "amazing-maze/lesson.md"]
    lessons = [p for p in lessons if p.exists()]
    if not lessons:
        print("no lesson.md files found")
        return 1
    for path in lessons:
        name = path.parent.name.replace("module-", "")
        out = OUT / f"{name}.ipynb"
        convert(path, out)
        print(f"wrote {out.relative_to(ROOT)} ({len(json.loads(out.read_text())['cells'])} cells)")
    # A top-level index notebook so `jupyter lab notebooks/` lands somewhere helpful.
    index_md = "# 42 Python Rank 2 — Notebook Index\n\n" + "\n".join(
        f"- [{p.stem}](./{p.name})"
        for p in sorted(OUT.glob("*.ipynb"))
    ) + "\n"
    (OUT / "00_index.ipynb").write_text(json.dumps({
        "cells": [_make_cell("markdown", index_md)],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
