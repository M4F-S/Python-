"""Top-level dispatch for the `course` command."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from . import commands


def _course_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="course",
        description=(
            "Self-paced CLI for the 42 Berlin Rank 2 Python course. "
            "Point it at a module/exercise (e.g. 05/ex1) and it opens "
            "the lesson, runs tests, or reveals the reference answer."
        ),
    )
    parser.add_argument(
        "--version", action="version",
        version=f"course {__version__}",
    )
    parser.add_argument(
        "--root", type=Path, default=_course_root(),
        help="Course root directory (defaults to installed location).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser(
        "status", help="Show progress across every module/exercise.",
    )
    p_status.set_defaults(func=commands.cmd_status)

    p_list = sub.add_parser(
        "list", help="List every module and exercise discoverable.",
    )
    p_list.set_defaults(func=commands.cmd_list)

    p_start = sub.add_parser(
        "start",
        help="Open an exercise (lesson.md + starter) in $EDITOR.",
    )
    p_start.add_argument("target", help="Module/exercise, e.g. '05/ex1'.")
    p_start.set_defaults(func=commands.cmd_start)

    p_check = sub.add_parser(
        "check",
        help="Run the pytest expectations for an exercise.",
    )
    p_check.add_argument(
        "target", nargs="?", default=None,
        help="Module/exercise (omit to check everything).",
    )
    p_check.set_defaults(func=commands.cmd_check)

    p_peek = sub.add_parser(
        "peek",
        help="Reveal the reference solution (records a peek event).",
    )
    p_peek.add_argument("target", help="Module/exercise, e.g. '05/ex1'.")
    p_peek.add_argument(
        "--reason", default="",
        help="Optional note about why the peek was needed.",
    )
    p_peek.set_defaults(func=commands.cmd_peek)

    p_diff = sub.add_parser(
        "diff",
        help="Show `diff exercises/<target> solutions/<target>`.",
    )
    p_diff.add_argument("target", help="Module/exercise, e.g. '05/ex1'.")
    p_diff.set_defaults(func=commands.cmd_diff)

    p_reset = sub.add_parser(
        "reset",
        help="Reset an exercise back to its starter state.",
    )
    p_reset.add_argument("target", help="Module/exercise, e.g. '05/ex1'.")
    p_reset.set_defaults(func=commands.cmd_reset)

    args = parser.parse_args(argv)
    try:
        return int(args.func(args) or 0)
    except BrokenPipeError:
        # Downstream pager / head closed the pipe - that's fine.
        return 0


if __name__ == "__main__":
    sys.exit(main())
