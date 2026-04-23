"""Course-wide smoke tests.

Run every reference solution and confirm that:
- it exits with the expected return code,
- its stdout contains every "canonical line" lifted straight from the
  subject PDFs.

Invoke with:
    pytest course/tests/

No extra config needed - uses the repo root as the working directory.
"""
from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


@dataclass(frozen=True)
class Case:
    label: str
    script: Path
    expect_rc: int = 0
    stdin: str | bytes | None = None
    cwd: Path | None = None
    must_contain: tuple[str, ...] = field(default_factory=tuple)
    args: tuple[str, ...] = ()


def _C(rel: str, *must: str, rc: int = 0, stdin: str | None = None,
       args: tuple[str, ...] = (), cwd: str | None = None) -> Case:
    script = REPO_ROOT / rel
    return Case(
        label=rel,
        script=script,
        expect_rc=rc,
        stdin=stdin,
        must_contain=must,
        args=args,
        cwd=(REPO_ROOT / cwd) if cwd else None,
    )


CASES: list[Case] = [
    # Module 00: the subject forbids "if __name__ == '__main__':" blocks,
    # so those scripts define functions without calling them. They are
    # exercised via import below (test_module00_*).

    # Module 01
    _C("module-01-oop/solutions/ex4/ft_garden_security.py"),
    _C("module-01-oop/solutions/ex6/ft_garden_analytics.py"),

    # Module 02
    _C("module-02-errors/solutions/ex3/ft_custom_errors.py"),
    _C("module-02-errors/solutions/ex4/ft_finally_block.py"),

    # Module 03
    _C("module-03-collections/solutions/ex5/ft_data_stream.py"),
    _C("module-03-collections/solutions/ex6/ft_data_alchemist.py"),

    # Module 04
    _C("module-04-fileio/solutions/ex3/ft_vault_security.py",
       "Cyber Archives Security"),

    # Module 05 (PDF canonical strings)
    _C("module-05-polymorphism/solutions/ex0/data_processor.py",
       "Got exception: Improper numeric data",
       "Numeric value 0: 1",
       "Text value 0: Hello",
       "Log entry 0: NOTICE: Connection to server"),
    _C("module-05-polymorphism/solutions/ex1/data_stream.py",
       "DataStream error - Can't process element in stream: Hello world",
       "Numeric Processor: total 4 items processed, remaining 4 on processor"),
    _C("module-05-polymorphism/solutions/ex2/data_pipeline.py",
       "CSV Output:", "JSON Output:"),

    # Module 06 - run from solutions/ so packages resolve
    _C("module-06-imports/solutions/ft_alembic_0.py",
       "Testing create_fire: Fire element created",
       cwd="module-06-imports/solutions"),
    _C("module-06-imports/solutions/ft_alembic_4.py",
       rc=1, cwd="module-06-imports/solutions"),
    _C("module-06-imports/solutions/ft_kaboom_0.py",
       "Spell recorded: Fantasy",
       cwd="module-06-imports/solutions"),
    _C("module-06-imports/solutions/ft_kaboom_1.py",
       rc=1, cwd="module-06-imports/solutions"),

    # Module 07
    _C("module-07-abstract/solutions/battle.py",
       "Flameling is a Fire type Creature",
       "Pyrodon is a Fire/Flying type Creature",
       cwd="module-07-abstract/solutions"),
    _C("module-07-abstract/solutions/capacitor.py",
       "Sproutling heals itself for a small amount",
       "Morphagon stabilizes its form.",
       cwd="module-07-abstract/solutions"),
    _C("module-07-abstract/solutions/tournament.py",
       "Battle error, aborting tournament: "
       "Invalid Creature 'Flameling' for this aggressive strategy",
       cwd="module-07-abstract/solutions"),

    # Module 08
    _C("module-08-matrix/solutions/ex0/construct.py"),
    _C("module-08-matrix/solutions/ex1/loading.py",
       cwd="module-08-matrix/solutions/ex1"),
    _C("module-08-matrix/solutions/ex2/oracle.py",
       "ORACLE STATUS"),

    # Module 09
    _C("module-09-pydantic/solutions/ex0/space_station.py",
       "Input should be less than or equal to 20"),
    _C("module-09-pydantic/solutions/ex1/alien_contact.py",
       "Telepathic contact requires at least 3 witnesses"),
    _C("module-09-pydantic/solutions/ex2/space_crew.py",
       "Mission must have at least one Commander or Captain"),

    # Module 10
    _C("module-10-functional/solutions/ex0/lambda_spells.py",
       "Fire Staff (92 power) comes before Crystal Orb (85 power)",
       "* fireball * * heal * * shield *"),
    _C("module-10-functional/solutions/ex1/higher_magic.py",
       "Combined spell result: Fireball hits Dragon, Heals Dragon",
       "Original: 10, Amplified: 30"),
    _C("module-10-functional/solutions/ex2/scope_mysteries.py",
       "counter_a call 2: 2", "counter_b call 1: 1",
       "Flaming Sword", "Frozen Shield",
       "Recall 'unknown': Memory not found"),
    _C("module-10-functional/solutions/ex3/functools_artifacts.py",
       "Sum: 100", "Product: 240000", "Max: 40",
       "Fib(10): 55",
       "Damage spell: 42 damage",
       "Enchantment: fireball",
       "Multi-cast: 3 spells",
       "Unknown spell type"),
    _C("module-10-functional/solutions/ex4/decorator_mastery.py",
       "Casting fireball...",
       "Spell casting failed after 3 attempts",
       "Successfully cast Lightning with 15 power",
       "Insufficient power for this spell"),
]


def _pdf_name(rel: str) -> str:
    # Turn "module-07-abstract/.../tournament.py" into "07 tournament.py".
    parts = rel.split("/")
    mod = parts[0].split("-")[1] if parts[0].startswith("module-") else parts[0]
    return f"{mod} {parts[-1]}"


@pytest.mark.parametrize(
    "case",
    CASES,
    ids=[_pdf_name(c.label) for c in CASES],
)
def test_solution(case: Case) -> None:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [PY, str(case.script), *case.args],
        cwd=str(case.cwd or case.script.parent),
        input=case.stdin,
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )
    assert proc.returncode == case.expect_rc, (
        f"{case.label} exited with {proc.returncode}, "
        f"expected {case.expect_rc}\nstdout:\n{proc.stdout}\n"
        f"stderr:\n{proc.stderr}"
    )
    for needle in case.must_contain:
        assert needle in proc.stdout, (
            f"{case.label} stdout missing {needle!r}\n"
            f"stdout:\n{proc.stdout}"
        )


def test_mazegen_wheel_is_valid() -> None:
    from zipfile import ZipFile

    wheel = REPO_ROOT / "amazing-maze/solutions/mazegen-1.0.0-py3-none-any.whl"
    assert wheel.is_file(), f"missing wheel: {wheel}"
    with ZipFile(wheel) as z:
        names = set(z.namelist())
    assert "mazegen/__init__.py" in names
    assert "mazegen/generator.py" in names


def test_mazegen_api() -> None:
    sys.path.insert(0, str(REPO_ROOT / "amazing-maze/solutions"))
    try:
        from mazegen import MazeGenerator, __version__
    finally:
        sys.path.pop(0)
    assert __version__ == "1.0.0"
    gen = MazeGenerator(width=6, height=4, seed=1, perfect=True)
    gen.generate()
    path = gen.shortest_path((0, 0), (5, 3))
    assert all(step in "NESW" for step in path)
    out = gen.encode_output((0, 0), (5, 3), path)
    assert out.endswith("\n")
    assert out.splitlines()[-1] == "".join(path)


# ---- Module 00 via import (subject forbids executing as a script) ----


import importlib.util
import io
from contextlib import redirect_stdout


def _load(rel: str):
    path = REPO_ROOT / rel
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _capture(fn, *args, stdin: str = "", **kwargs) -> str:
    buf = io.StringIO()
    old = sys.stdin
    sys.stdin = io.StringIO(stdin)
    try:
        with redirect_stdout(buf):
            fn(*args, **kwargs)
    finally:
        sys.stdin = old
    return buf.getvalue()


def test_module00_hello_garden() -> None:
    mod = _load("module-00-fundamentals/solutions/ex0/ft_hello_garden.py")
    out = _capture(mod.ft_hello_garden)
    assert "Garden" in out


def test_module00_garden_name() -> None:
    mod = _load("module-00-fundamentals/solutions/ex1/ft_garden_name.py")
    out = _capture(mod.ft_garden_name, stdin="MyGarden\n")
    assert "MyGarden" in out
    assert "Status: Growing well!" in out


def test_module00_plot_area() -> None:
    mod = _load("module-00-fundamentals/solutions/ex2/ft_plot_area.py")
    out = _capture(mod.ft_plot_area, stdin="3\n4\n")
    assert "12" in out


def test_module00_harvest_total() -> None:
    mod = _load("module-00-fundamentals/solutions/ex3/ft_harvest_total.py")
    out = _capture(mod.ft_harvest_total, stdin="1\n2\n3\n")
    assert "6" in out


def test_module00_plant_age() -> None:
    mod = _load("module-00-fundamentals/solutions/ex4/ft_plant_age.py")
    assert "ready to harvest" in _capture(mod.ft_plant_age, stdin="90\n")
    assert "more time" in _capture(mod.ft_plant_age, stdin="10\n")


def test_module00_water_reminder() -> None:
    mod = _load("module-00-fundamentals/solutions/ex5/ft_water_reminder.py")
    assert "Water" in _capture(mod.ft_water_reminder, stdin="5\n")
    assert "fine" in _capture(mod.ft_water_reminder, stdin="1\n")


def test_module00_count_harvest_iterative() -> None:
    mod = _load(
        "module-00-fundamentals/solutions/ex6/ft_count_harvest_iterative.py"
    )
    out = _capture(mod.ft_count_harvest_iterative, stdin="3\n")
    for line in ("Day 1", "Day 2", "Day 3", "Harvest time!"):
        assert line in out


def test_module00_count_harvest_recursive() -> None:
    mod = _load(
        "module-00-fundamentals/solutions/ex6/ft_count_harvest_recursive.py"
    )
    out = _capture(mod.ft_count_harvest_recursive, stdin="3\n")
    for line in ("Day 1", "Day 2", "Day 3", "Harvest time!"):
        assert line in out


def test_module00_seed_inventory() -> None:
    mod = _load("module-00-fundamentals/solutions/ex7/ft_seed_inventory.py")
    out = _capture(mod.ft_seed_inventory, "carrot", 5, "packets")
    assert "Carrot seeds: 5 packets available" in out
    out = _capture(mod.ft_seed_inventory, "lettuce", 250, "grams")
    assert "Lettuce seeds: 250 grams total" in out
    out = _capture(mod.ft_seed_inventory, "sunflower", 10, "area")
    assert "Sunflower seeds: covers 10 square meters" in out
