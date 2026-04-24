"""Discover modules and exercises under the course root."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


MODULE_RE = re.compile(r"^module-(\d{2})-(.+)$")


@dataclass(frozen=True)
class Module:
    number: str           # "05"
    slug: str             # "polymorphism"
    dir: Path             # absolute path
    lesson: Path | None   # lesson.md
    subject_pdf: Path | None


@dataclass(frozen=True)
class Exercise:
    module: Module
    name: str                      # "ex1"
    starter_dir: Path              # course/.../exercises/ex1 or exercises/
    solution_dir: Path | None
    id: str                        # "05/ex1"


def iter_modules(root: Path) -> list[Module]:
    mods: list[Module] = []
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        match = MODULE_RE.match(child.name)
        if match:
            lesson = child / "lesson.md"
            pdf = child / "subject.pdf"
            mods.append(
                Module(
                    number=match.group(1),
                    slug=match.group(2),
                    dir=child,
                    lesson=lesson if lesson.exists() else None,
                    subject_pdf=pdf if pdf.exists() else None,
                )
            )
    # The Amazing project doesn't follow the module-NN-* pattern.
    amazing = root / "amazing-maze"
    if amazing.is_dir():
        mods.append(
            Module(
                number="AM",
                slug="amazing-maze",
                dir=amazing,
                lesson=(amazing / "lesson.md") if (amazing / "lesson.md").exists() else None,
                subject_pdf=(amazing / "subject.pdf") if (amazing / "subject.pdf").exists() else None,
            )
        )
    return mods


def iter_exercises(module: Module) -> list[Exercise]:
    starters = module.dir / "exercises"
    solutions = module.dir / "solutions"
    if not starters.exists():
        return []
    # Two layouts exist:
    #   <module>/exercises/exN/*.py   (most modules)
    #   <module>/exercises/*.py       (module 06: flat tree)
    exercises: list[Exercise] = []
    sub_ex_dirs = sorted(
        p for p in starters.iterdir()
        if p.is_dir() and p.name.startswith("ex")
    )
    if sub_ex_dirs:
        for d in sub_ex_dirs:
            exercises.append(
                Exercise(
                    module=module,
                    name=d.name,
                    starter_dir=d,
                    solution_dir=(solutions / d.name) if (solutions / d.name).exists() else None,
                    id=f"{module.number}/{d.name}",
                )
            )
    else:
        exercises.append(
            Exercise(
                module=module,
                name="all",
                starter_dir=starters,
                solution_dir=solutions if solutions.exists() else None,
                id=f"{module.number}/all",
            )
        )
    return exercises


def find(root: Path, target: str) -> Exercise | None:
    """Parse '05/ex1' or '05-ex1' or 'AM' into an Exercise."""
    normalised = target.replace("-", "/").replace(".", "/")
    for mod in iter_modules(root):
        for ex in iter_exercises(mod):
            if ex.id == normalised or ex.id.lower() == normalised.lower():
                return ex
            if mod.number == normalised and ex.name == "all":
                return ex
    return None


def find_module(root: Path, target: str) -> Module | None:
    for mod in iter_modules(root):
        if mod.number == target or mod.slug == target:
            return mod
    return None
