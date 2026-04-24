"""Command implementations for the `course` CLI."""
from __future__ import annotations

import argparse
import difflib
import os
import shutil
import subprocess
import sys
from pathlib import Path

from . import discover, progress


def _fail(msg: str) -> int:
    print(f"course: {msg}", file=sys.stderr)
    return 1


def _ok(msg: str) -> None:
    print(msg)


def cmd_list(args: argparse.Namespace) -> int:
    for mod in discover.iter_modules(args.root):
        print(f"{mod.number}  {mod.slug}")
        for ex in discover.iter_exercises(mod):
            print(f"    {ex.id}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    data = progress.load(args.root)
    exercises = data.get("exercises", {})
    peeks = data.get("peeks", [])
    done = sum(1 for v in exercises.values() if v.get("status") == "done")
    total = sum(len(discover.iter_exercises(m)) for m in discover.iter_modules(args.root))
    bar_width = 30
    filled = int(bar_width * (done / total)) if total else 0
    bar = "█" * filled + "·" * (bar_width - filled)
    _ok(f"Progress: [{bar}] {done}/{total} exercises")
    if peeks:
        _ok(f"Peeks:    {len(peeks)}")
    _ok("")
    for mod in discover.iter_modules(args.root):
        exs = discover.iter_exercises(mod)
        if not exs:
            continue
        _ok(f"{mod.number} {mod.slug}")
        for ex in exs:
            record = exercises.get(ex.id, {})
            status = record.get("status", "   ")
            peek_count = record.get("peeks", 0)
            badge = {"done": "✓", "in_progress": "•", "peeked": "👀"}.get(
                status, " "
            )
            suffix = f"  (peeked ×{peek_count})" if peek_count else ""
            _ok(f"  [{badge}] {ex.id}{suffix}")
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    ex = discover.find(args.root, args.target)
    if ex is None:
        return _fail(f"unknown target: {args.target!r}. Try `course list`.")
    lesson = ex.module.lesson
    starter_files = sorted(ex.starter_dir.rglob("*.py"))
    subject = ex.module.subject_pdf

    _ok(f"Module {ex.module.number} — {ex.module.slug}")
    _ok(f"  lesson:  {lesson}" if lesson else "  lesson:  (none)")
    _ok(f"  subject: {subject}" if subject else "  subject: (none)")
    _ok("  starter files:")
    for f in starter_files:
        _ok(f"    {f}")

    editor = os.environ.get("EDITOR")
    if editor and starter_files:
        paths: list[str] = []
        if lesson:
            paths.append(str(lesson))
        paths.extend(str(p) for p in starter_files)
        try:
            subprocess.call([editor, *paths])
        except FileNotFoundError:
            _ok(f"(could not launch {editor!r} — open the files manually)")

    progress.mark(args.root, ex.id, "in_progress")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    tests_dir = args.root / "tests"
    if not tests_dir.exists():
        return _fail("no tests/ directory under course root")
    cmd = [sys.executable, "-m", "pytest", "-q", str(tests_dir)]
    if args.target:
        ex = discover.find(args.root, args.target)
        if ex is None:
            return _fail(f"unknown target: {args.target!r}")
        cmd.extend(["-k", args.target.replace("/", " ")])
    result = subprocess.run(cmd, cwd=str(args.root))
    if args.target and result.returncode == 0:
        progress.mark(args.root, args.target, "done")
    return result.returncode


def cmd_peek(args: argparse.Namespace) -> int:
    ex = discover.find(args.root, args.target)
    if ex is None:
        return _fail(f"unknown target: {args.target!r}")
    if ex.solution_dir is None or not ex.solution_dir.exists():
        return _fail(f"no solution recorded for {ex.id}")
    progress.record_peek(args.root, ex.id, reason=args.reason)
    _ok(f"⚠ Revealing solution for {ex.id} — logged in .course-progress.json.")
    for f in sorted(ex.solution_dir.rglob("*.py")):
        _ok(f"")
        _ok(f"=== {f.relative_to(args.root)} ===")
        _ok(f.read_text())
    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    ex = discover.find(args.root, args.target)
    if ex is None:
        return _fail(f"unknown target: {args.target!r}")
    if ex.solution_dir is None:
        return _fail(f"no solution recorded for {ex.id}")
    solution_files = {
        p.relative_to(ex.solution_dir): p
        for p in ex.solution_dir.rglob("*.py")
    }
    starter_files = {
        p.relative_to(ex.starter_dir): p
        for p in ex.starter_dir.rglob("*.py")
    }
    for rel, sol in sorted(solution_files.items()):
        starter = starter_files.get(rel)
        if starter is None:
            _ok(f"[only in solution] {rel}")
            continue
        a_lines = starter.read_text().splitlines(keepends=True)
        b_lines = sol.read_text().splitlines(keepends=True)
        diff = difflib.unified_diff(
            a_lines, b_lines,
            fromfile=f"exercises/{rel}",
            tofile=f"solutions/{rel}",
        )
        sys.stdout.writelines(diff)
    return 0


def cmd_reset(args: argparse.Namespace) -> int:
    ex = discover.find(args.root, args.target)
    if ex is None:
        return _fail(f"unknown target: {args.target!r}")
    answer = input(
        f"Reset all files under {ex.starter_dir} to their git HEAD? [y/N] "
    )
    if answer.strip().lower() != "y":
        _ok("aborted.")
        return 0
    try:
        subprocess.check_call(
            ["git", "checkout", "--", str(ex.starter_dir)],
            cwd=str(args.root.parent),
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        return _fail(f"git checkout failed: {exc}")
    progress.mark(args.root, ex.id, "reset")
    _ok(f"Reset {ex.id}.")
    return 0
