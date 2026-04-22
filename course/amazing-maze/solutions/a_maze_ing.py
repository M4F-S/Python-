"""Entry-point script for the A-Maze-ing project.

Usage:
    python3 a_maze_ing.py config.txt
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from mazegen import MazeGenerationError, MazeGenerator

# The "42" stencil - 5 rows x 9 cols. '#' = cell must remain fully walled.
_42_PATTERN = (
    "####.####",
    "#..#.#..#",
    "####.####",
    "...#....#",
    "...#....#",
)


class MazeConfigError(Exception):
    pass


class MazeConfig:
    """Tiny hand-rolled config, validated in-place."""

    REQUIRED_KEYS = (
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    )

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        output_file: str,
        perfect: bool,
        seed: Optional[int] = None,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        self._validate()

    def _validate(self) -> None:
        if self.width < 2 or self.height < 2:
            raise MazeConfigError(
                f"WIDTH and HEIGHT must be >= 2 (got "
                f"{self.width}x{self.height})"
            )
        for name, cell in (("ENTRY", self.entry), ("EXIT", self.exit)):
            x, y = cell
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise MazeConfigError(
                    f"{name} {cell} is outside "
                    f"{self.width}x{self.height} maze"
                )
        if self.entry == self.exit:
            raise MazeConfigError("ENTRY and EXIT must be distinct")

    @classmethod
    def from_file(cls, path: str) -> "MazeConfig":
        data: dict[str, str] = {}
        p = Path(path)
        try:
            raw = p.read_text(encoding="utf-8")
        except OSError as exc:
            raise MazeConfigError(
                f"Cannot read config file {path!r}: {exc}"
            ) from exc
        for line_no, line in enumerate(raw.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "=" not in stripped:
                raise MazeConfigError(
                    f"{path}:{line_no}: missing '=' in line {line!r}"
                )
            key, _, value = stripped.partition("=")
            data[key.strip().upper()] = value.strip()

        missing = [k for k in cls.REQUIRED_KEYS if k not in data]
        if missing:
            raise MazeConfigError(
                f"Missing config keys: {', '.join(missing)}"
            )

        try:
            width = int(data["WIDTH"])
            height = int(data["HEIGHT"])
        except ValueError as exc:
            raise MazeConfigError(
                f"WIDTH and HEIGHT must be integers: {exc}"
            ) from exc

        entry = _parse_coord(data["ENTRY"], "ENTRY")
        exit_ = _parse_coord(data["EXIT"], "EXIT")
        perfect = _parse_bool(data["PERFECT"], "PERFECT")
        seed_raw = data.get("SEED")
        seed: Optional[int]
        if seed_raw is None:
            seed = None
        else:
            try:
                seed = int(seed_raw)
            except ValueError as exc:
                raise MazeConfigError(
                    f"SEED must be an integer: {seed_raw!r}"
                ) from exc

        return cls(
            width=width,
            height=height,
            entry=entry,
            exit_=exit_,
            output_file=data["OUTPUT_FILE"],
            perfect=perfect,
            seed=seed,
        )


def _parse_coord(value: str, name: str) -> tuple[int, int]:
    try:
        x_str, y_str = value.split(",")
        return (int(x_str.strip()), int(y_str.strip()))
    except (ValueError, IndexError) as exc:
        raise MazeConfigError(
            f"{name} must look like 'x,y' (got {value!r}): {exc}"
        ) from exc


def _parse_bool(value: str, name: str) -> bool:
    lowered = value.strip().lower()
    if lowered in ("true", "1", "yes", "y"):
        return True
    if lowered in ("false", "0", "no", "n"):
        return False
    raise MazeConfigError(
        f"{name} must be True or False (got {value!r})"
    )


def forbidden_cells_for_42(width: int, height: int) -> set[tuple[int, int]]:
    """Return the cells the '42' stencil covers, centred in the maze.

    Returns an empty set if the maze is too small to fit the stencil
    (in which case the caller prints a warning).
    """
    pattern_height = len(_42_PATTERN)
    pattern_width = len(_42_PATTERN[0])
    if width < pattern_width + 2 or height < pattern_height + 2:
        return set()
    x0 = (width - pattern_width) // 2
    y0 = (height - pattern_height) // 2
    cells: set[tuple[int, int]] = set()
    for dy, row in enumerate(_42_PATTERN):
        for dx, ch in enumerate(row):
            if ch == "#":
                cells.add((x0 + dx, y0 + dy))
    return cells


def build_generator(cfg: MazeConfig) -> MazeGenerator:
    forbidden = forbidden_cells_for_42(cfg.width, cfg.height)
    if not forbidden:
        print(
            "[warn] maze too small to draw the '42' pattern, skipping",
            file=sys.stderr,
        )
    if cfg.entry in forbidden or cfg.exit in forbidden:
        raise MazeConfigError(
            "ENTRY or EXIT overlaps the '42' pattern - "
            "move them or shrink the maze"
        )
    return MazeGenerator(
        width=cfg.width,
        height=cfg.height,
        seed=cfg.seed,
        perfect=cfg.perfect,
        forbidden=forbidden,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} <config.txt>", file=sys.stderr)
        return 2
    try:
        cfg = MazeConfig.from_file(argv[1])
        gen = build_generator(cfg)
        gen.generate()
        path = gen.shortest_path(cfg.entry, cfg.exit)
    except (MazeConfigError, MazeGenerationError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        Path(cfg.output_file).write_text(
            gen.encode_output(cfg.entry, cfg.exit, path),
            encoding="utf-8",
        )
    except OSError as exc:
        print(
            f"error: cannot write {cfg.output_file!r}: {exc}",
            file=sys.stderr,
        )
        return 1

    print(gen.render_ascii(entry=cfg.entry, exit_=cfg.exit, path=path))
    print()
    print(f"entry: {cfg.entry}")
    print(f"exit:  {cfg.exit}")
    print(f"path:  {''.join(path)} ({len(path)} steps)")
    print(f"saved to: {cfg.output_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
