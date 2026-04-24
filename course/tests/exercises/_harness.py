"""Shared harness for per-exercise tests.

The solution tests live in `tests/test_all_solutions.py` and run
against `solutions/`. These exercise tests run the same expectations
against `exercises/` so students can use `course check 05/ex1` (or
plain `pytest tests/exercises/ -k 05`) to get instant feedback while
they implement.

Each per-exercise test file imports CASES from here, picks the case
that matches its module/exercise, and swaps `solutions/` for
`exercises/` in the path. If the student's code is still a TODO stub
(the default starter), the test fails with a clean message — that's
the intended signal.
"""
from __future__ import annotations

import importlib.util
import io
import os
import subprocess
import sys
from contextlib import redirect_stdout
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable


@dataclass(frozen=True)
class ExerciseExpectation:
    """A single module/exercise run expectation."""
    module: str                      # "module-05-polymorphism"
    path: str                        # "ex0/data_processor.py"
    must_contain: tuple[str, ...] = field(default_factory=tuple)
    expect_rc: int = 0
    stdin: str | None = None
    args: tuple[str, ...] = ()
    cwd: str | None = None

    def run_against(self, flavour: str) -> tuple[int, str, str]:
        """Run this expectation against solutions/ or exercises/.

        Returns (returncode, stdout, stderr).
        """
        assert flavour in {"solutions", "exercises"}
        script = REPO_ROOT / self.module / flavour / self.path
        cwd = REPO_ROOT / self.cwd if self.cwd else script.parent
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        proc = subprocess.run(
            [PY, str(script), *self.args],
            cwd=str(cwd),
            input=self.stdin,
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
        )
        return proc.returncode, proc.stdout, proc.stderr


def assert_expectation(exp: ExerciseExpectation, flavour: str) -> None:
    script = REPO_ROOT / exp.module / flavour / exp.path
    if not script.exists():
        import pytest
        pytest.skip(f"{script.relative_to(REPO_ROOT)} not found")
    rc, stdout, stderr = exp.run_against(flavour)
    assert rc == exp.expect_rc, (
        f"{exp.module}/{flavour}/{exp.path} exited {rc}, expected {exp.expect_rc}\n"
        f"stdout:\n{stdout}\nstderr:\n{stderr}"
    )
    for needle in exp.must_contain:
        assert needle in stdout, (
            f"{exp.module}/{flavour}/{exp.path} stdout missing {needle!r}\n"
            f"stdout:\n{stdout}"
        )


@dataclass(frozen=True)
class FunctionExpectation:
    """For Module 00: load a function by name and call it with stdin."""
    module: str                       # "module-00-fundamentals"
    path: str                         # "ex0/ft_hello_garden.py"
    function: str                     # "ft_hello_garden"
    args: tuple = ()
    stdin: str = ""
    must_contain: tuple[str, ...] = field(default_factory=tuple)

    def load(self, flavour: str) -> ModuleType:
        script = REPO_ROOT / self.module / flavour / self.path
        spec = importlib.util.spec_from_file_location(
            f"{flavour}_{script.stem}", script,
        )
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def run(self, flavour: str) -> str:
        mod = self.load(flavour)
        fn = getattr(mod, self.function, None)
        if fn is None:
            raise AssertionError(
                f"{self.module}/{flavour}/{self.path} is missing "
                f"function {self.function!r}"
            )
        buf = io.StringIO()
        old_stdin = sys.stdin
        sys.stdin = io.StringIO(self.stdin)
        try:
            with redirect_stdout(buf):
                fn(*self.args)
        finally:
            sys.stdin = old_stdin
        return buf.getvalue()


def assert_function(exp: FunctionExpectation, flavour: str) -> None:
    script = REPO_ROOT / exp.module / flavour / exp.path
    if not script.exists():
        import pytest
        pytest.skip(f"{script.relative_to(REPO_ROOT)} not found")
    out = exp.run(flavour)
    for needle in exp.must_contain:
        assert needle in out, (
            f"{exp.module}/{flavour}/{exp.path}::{exp.function} "
            f"stdout missing {needle!r}\nstdout:\n{out}"
        )
