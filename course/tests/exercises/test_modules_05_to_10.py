"""Per-exercise tests for Modules 05 through 10."""
from ._harness import ExerciseExpectation, assert_expectation

CASES = [
    # Module 05 - canonical strings straight from py-05.pdf.
    ExerciseExpectation(
        "module-05-polymorphism", "ex0/data_processor.py",
        must_contain=(
            "Got exception: Improper numeric data",
            "Numeric value 0: 1",
            "Text value 0: Hello",
            "Log entry 0: NOTICE: Connection to server",
        ),
    ),
    ExerciseExpectation(
        "module-05-polymorphism", "ex1/data_stream.py",
        must_contain=(
            "DataStream error - Can't process element in stream: Hello world",
            "Numeric Processor: total 4 items processed, "
            "remaining 4 on processor",
        ),
    ),
    ExerciseExpectation(
        "module-05-polymorphism", "ex2/data_pipeline.py",
        must_contain=("CSV Output:", "JSON Output:"),
    ),

    # Module 06 (scripts run from <module>/exercises/)
    ExerciseExpectation(
        "module-06-imports", "ft_alembic_0.py",
        must_contain=("Testing create_fire: Fire element created",),
        cwd="module-06-imports/exercises",
    ),
    ExerciseExpectation(
        "module-06-imports", "ft_distillation_0.py",
        must_contain=(
            "Testing strength_potion: Strength potion brewed with "
            "'Fire element created' and 'Water element created'",
        ),
        cwd="module-06-imports/exercises",
    ),
    ExerciseExpectation(
        "module-06-imports", "ft_kaboom_0.py",
        must_contain=("Spell recorded: Fantasy",),
        cwd="module-06-imports/exercises",
    ),

    # Module 07
    ExerciseExpectation(
        "module-07-abstract", "battle.py",
        must_contain=(
            "Flameling is a Fire type Creature",
            "Pyrodon is a Fire/Flying type Creature",
        ),
        cwd="module-07-abstract/exercises",
    ),
    ExerciseExpectation(
        "module-07-abstract", "capacitor.py",
        must_contain=(
            "Sproutling heals itself for a small amount",
            "Morphagon stabilizes its form.",
        ),
        cwd="module-07-abstract/exercises",
    ),
    ExerciseExpectation(
        "module-07-abstract", "tournament.py",
        must_contain=(
            "Battle error, aborting tournament: "
            "Invalid Creature 'Flameling' for this aggressive strategy",
        ),
        cwd="module-07-abstract/exercises",
    ),

    # Module 08
    ExerciseExpectation(
        "module-08-matrix", "ex0/construct.py",
        must_contain=("MATRIX STATUS",),
    ),

    # Module 09
    ExerciseExpectation(
        "module-09-pydantic", "ex0/space_station.py",
        must_contain=("Input should be less than or equal to 20",),
    ),
    ExerciseExpectation(
        "module-09-pydantic", "ex1/alien_contact.py",
        must_contain=("Telepathic contact requires at least 3 witnesses",),
    ),
    ExerciseExpectation(
        "module-09-pydantic", "ex2/space_crew.py",
        must_contain=("Mission must have at least one Commander or Captain",),
    ),

    # Module 10
    ExerciseExpectation(
        "module-10-functional", "ex0/lambda_spells.py",
        must_contain=(
            "Fire Staff (92 power) comes before Crystal Orb (85 power)",
            "* fireball * * heal * * shield *",
        ),
    ),
    ExerciseExpectation(
        "module-10-functional", "ex1/higher_magic.py",
        must_contain=(
            "Combined spell result: Fireball hits Dragon, Heals Dragon",
            "Original: 10, Amplified: 30",
        ),
    ),
    ExerciseExpectation(
        "module-10-functional", "ex2/scope_mysteries.py",
        must_contain=(
            "counter_a call 2: 2",
            "counter_b call 1: 1",
            "Flaming Sword",
            "Frozen Shield",
            "Recall 'unknown': Memory not found",
        ),
    ),
    ExerciseExpectation(
        "module-10-functional", "ex3/functools_artifacts.py",
        must_contain=(
            "Sum: 100", "Product: 240000", "Max: 40",
            "Fib(10): 55",
            "Damage spell: 42 damage",
            "Enchantment: fireball",
            "Multi-cast: 3 spells",
            "Unknown spell type",
        ),
    ),
    ExerciseExpectation(
        "module-10-functional", "ex4/decorator_mastery.py",
        must_contain=(
            "Casting fireball...",
            "Spell casting failed after 3 attempts",
            "Successfully cast Lightning with 15 power",
            "Insufficient power for this spell",
        ),
    ),
]


def pytest_generate_tests(metafunc):  # type: ignore[no-untyped-def]
    if "case" in metafunc.fixturenames:
        metafunc.parametrize(
            "case", CASES,
            ids=[f"{c.module.split('-')[1]}/{c.path}" for c in CASES],
        )


def test_exercise(case: ExerciseExpectation) -> None:
    assert_expectation(case, "exercises")
