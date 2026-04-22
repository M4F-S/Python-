"""Core maze generation logic - randomised recursive backtracker."""
from __future__ import annotations

import random
from collections import deque
from typing import Iterable, Optional


# Wall bit layout: bit 0=N, 1=E, 2=S, 3=W. Wall closed = bit set.
N, E, S, W = 1, 2, 4, 8
ALL_WALLS = N | E | S | W

_OPPOSITE = {N: S, S: N, E: W, W: E}
_DELTA = {N: (0, -1), S: (0, 1), E: (1, 0), W: (-1, 0)}
_LETTER = {N: "N", E: "E", S: "S", W: "W"}


class MazeGenerationError(Exception):
    """Raised when the requested maze cannot be generated."""


Coord = tuple[int, int]


class MazeGenerator:
    """Generate a (possibly perfect) maze.

    Parameters
    ----------
    width, height:
        Maze dimensions in cells. Both must be >= 1.
    seed:
        Optional random seed for reproducibility.
    perfect:
        If True, the maze has exactly one path between any two
        non-forbidden cells. If False, a handful of extra openings are
        carved after the perfect phase.
    forbidden:
        Cells that must remain fully walled (used to draw the '42'
        pattern). The generator never enters these cells.
    """

    def __init__(
        self,
        width: int,
        height: int,
        *,
        seed: Optional[int] = None,
        perfect: bool = True,
        forbidden: Optional[Iterable[Coord]] = None,
    ) -> None:
        if width < 1 or height < 1:
            raise MazeGenerationError(
                f"Invalid maze dimensions: {width}x{height}"
            )
        self.width = width
        self.height = height
        self.perfect = perfect
        self.seed = seed
        self._forbidden: set[Coord] = set(forbidden or ())
        self._rng = random.Random(seed)
        self.cells: list[list[int]] = [
            [ALL_WALLS for _ in range(width)] for _ in range(height)
        ]
        self._generated = False

    # ---- public API ----------------------------------------------------

    def generate(self) -> None:
        """Carve the maze in-place."""
        start = self._first_open_cell()
        if start is None:
            raise MazeGenerationError(
                "Every cell is forbidden; nothing to generate"
            )
        self._recursive_backtracker(start)
        if not self.perfect:
            self._add_loops()
        self._assert_no_open_3x3()
        self._generated = True

    def shortest_path(self, entry: Coord, exit_: Coord) -> list[str]:
        """BFS shortest path; returns a list of N/E/S/W letters."""
        self._require_generated()
        self._require_in_bounds(entry, "entry")
        self._require_in_bounds(exit_, "exit")
        if entry in self._forbidden or exit_ in self._forbidden:
            raise MazeGenerationError(
                "Entry or exit coincides with a forbidden cell"
            )
        if entry == exit_:
            return []
        parents: dict[Coord, tuple[Coord, int]] = {}
        queue: deque[Coord] = deque([entry])
        visited: set[Coord] = {entry}
        while queue:
            cell = queue.popleft()
            if cell == exit_:
                break
            for direction in (N, E, S, W):
                if self._has_wall(cell, direction):
                    continue
                dx, dy = _DELTA[direction]
                nxt = (cell[0] + dx, cell[1] + dy)
                if nxt in visited or nxt in self._forbidden:
                    continue
                visited.add(nxt)
                parents[nxt] = (cell, direction)
                queue.append(nxt)
        if exit_ not in parents and exit_ != entry:
            raise MazeGenerationError(
                "No path between entry and exit"
            )
        letters: list[str] = []
        cursor = exit_
        while cursor != entry:
            prev, direction = parents[cursor]
            letters.append(_LETTER[direction])
            cursor = prev
        letters.reverse()
        return letters

    def render_ascii(
        self,
        entry: Optional[Coord] = None,
        exit_: Optional[Coord] = None,
        path: Optional[list[str]] = None,
    ) -> str:
        """Render the maze as an ASCII string.

        '#' = wall cell, ' ' = open cell, 'E'/'X' = entry/exit,
        '.' = cell on the solution path, '*' = forbidden (42) cell.
        """
        self._require_generated()
        path_cells: set[Coord] = set()
        if entry is not None and path is not None:
            cx, cy = entry
            path_cells.add((cx, cy))
            for step in path:
                dx, dy = _DELTA[_letter_to_bit(step)]
                cx += dx
                cy += dy
                path_cells.add((cx, cy))

        rows: list[str] = []
        # top border
        top = "+" + "---+" * self.width
        rows.append(top)
        for y in range(self.height):
            mid = "|"
            bot = "+"
            for x in range(self.width):
                cell = (x, y)
                glyph = "   "
                if cell in self._forbidden:
                    glyph = "***"
                elif entry is not None and cell == entry:
                    glyph = " E "
                elif exit_ is not None and cell == exit_:
                    glyph = " X "
                elif cell in path_cells:
                    glyph = " . "
                mid += glyph
                mid += "|" if self._has_wall(cell, E) else " "
                bot += "---" if self._has_wall(cell, S) else "   "
                bot += "+"
            rows.append(mid)
            rows.append(bot)
        return "\n".join(rows)

    def encode_output(
        self,
        entry: Coord,
        exit_: Coord,
        path: list[str],
    ) -> str:
        """Format the subject-mandated output file content."""
        self._require_generated()
        lines: list[str] = []
        for y in range(self.height):
            lines.append(
                "".join(format(self.cells[y][x], "x") for x in range(self.width))
            )
        lines.append("")
        lines.append(f"{entry[0]},{entry[1]}")
        lines.append(f"{exit_[0]},{exit_[1]}")
        lines.append("".join(path))
        return "\n".join(lines) + "\n"

    # ---- internals -----------------------------------------------------

    def _has_wall(self, cell: Coord, direction: int) -> bool:
        x, y = cell
        return bool(self.cells[y][x] & direction)

    def _carve(self, a: Coord, b: Coord) -> None:
        ax, ay = a
        bx, by = b
        dx, dy = bx - ax, by - ay
        if (dx, dy) == (0, -1):
            self.cells[ay][ax] &= ~N
            self.cells[by][bx] &= ~S
        elif (dx, dy) == (0, 1):
            self.cells[ay][ax] &= ~S
            self.cells[by][bx] &= ~N
        elif (dx, dy) == (1, 0):
            self.cells[ay][ax] &= ~E
            self.cells[by][bx] &= ~W
        elif (dx, dy) == (-1, 0):
            self.cells[ay][ax] &= ~W
            self.cells[by][bx] &= ~E
        else:
            raise MazeGenerationError(
                f"Cannot carve between non-adjacent cells {a} and {b}"
            )

    def _recursive_backtracker(self, start: Coord) -> None:
        stack: list[Coord] = [start]
        visited: set[Coord] = {start}
        while stack:
            current = stack[-1]
            candidates: list[Coord] = []
            for direction in (N, E, S, W):
                dx, dy = _DELTA[direction]
                nxt = (current[0] + dx, current[1] + dy)
                if not self._in_bounds(nxt):
                    continue
                if nxt in visited or nxt in self._forbidden:
                    continue
                candidates.append(nxt)
            if not candidates:
                stack.pop()
                continue
            chosen = self._rng.choice(candidates)
            self._carve(current, chosen)
            visited.add(chosen)
            stack.append(chosen)

    def _add_loops(self) -> None:
        """Knock down ~5% of extra internal walls (non-perfect mode)."""
        removable: list[tuple[Coord, int]] = []
        for y in range(self.height):
            for x in range(self.width):
                cell = (x, y)
                if cell in self._forbidden:
                    continue
                for direction in (E, S):
                    if not self._has_wall(cell, direction):
                        continue
                    dx, dy = _DELTA[direction]
                    nxt = (x + dx, y + dy)
                    if not self._in_bounds(nxt):
                        continue
                    if nxt in self._forbidden:
                        continue
                    removable.append((cell, direction))
        self._rng.shuffle(removable)
        budget = max(1, len(removable) // 20)
        for cell, direction in removable:
            if budget <= 0:
                break
            dx, dy = _DELTA[direction]
            neighbour = (cell[0] + dx, cell[1] + dy)
            backup_a = self.cells[cell[1]][cell[0]]
            backup_b = self.cells[neighbour[1]][neighbour[0]]
            self._carve(cell, neighbour)
            if self._has_open_3x3():
                self.cells[cell[1]][cell[0]] = backup_a
                self.cells[neighbour[1]][neighbour[0]] = backup_b
                continue
            budget -= 1

    def _has_open_3x3(self) -> bool:
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                ok = True
                for dy in range(3):
                    for dx in range(3):
                        c = (x + dx, y + dy)
                        if c in self._forbidden:
                            ok = False
                            break
                        # Cell is "open" if all internal walls between the
                        # 3x3 block cells are down. Check: every inner
                        # edge within the 3x3 must be open.
                    if not ok:
                        break
                if not ok:
                    continue
                # Check all 12 internal edges are open.
                clear = True
                for dy in range(3):
                    for dx in range(3):
                        cx, cy = x + dx, y + dy
                        if dx < 2 and self._has_wall((cx, cy), E):
                            clear = False
                            break
                        if dy < 2 and self._has_wall((cx, cy), S):
                            clear = False
                            break
                    if not clear:
                        break
                if clear:
                    return True
        return False

    def _assert_no_open_3x3(self) -> None:
        if self._has_open_3x3():
            raise MazeGenerationError(
                "Generated maze contains a 3x3 open area"
            )

    def _first_open_cell(self) -> Optional[Coord]:
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self._forbidden:
                    return (x, y)
        return None

    def _in_bounds(self, cell: Coord) -> bool:
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def _require_in_bounds(self, cell: Coord, name: str) -> None:
        if not self._in_bounds(cell):
            raise MazeGenerationError(
                f"{name} {cell} is outside {self.width}x{self.height} maze"
            )

    def _require_generated(self) -> None:
        if not self._generated:
            raise MazeGenerationError(
                "Call .generate() before using this method"
            )


def _letter_to_bit(letter: str) -> int:
    return {"N": N, "E": E, "S": S, "W": W}[letter]
