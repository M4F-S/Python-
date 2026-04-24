"""Per-exercise tests for Modules 01-04."""
from ._harness import ExerciseExpectation, assert_expectation

CASES = [
    # Module 01 - each solution script prints a descriptive header.
    ExerciseExpectation(
        "module-01-oop", "ex4/ft_garden_security.py",
        must_contain=("Garden Security",),
    ),
    ExerciseExpectation(
        "module-01-oop", "ex6/ft_garden_analytics.py",
        must_contain=("Garden Analytics",),
    ),

    # Module 02
    ExerciseExpectation(
        "module-02-errors", "ex3/ft_custom_errors.py",
        must_contain=("Plant Error Handling",),
    ),
    ExerciseExpectation(
        "module-02-errors", "ex4/ft_finally_block.py",
        must_contain=("Watering System Test",),
    ),

    # Module 03
    ExerciseExpectation(
        "module-03-collections", "ex5/ft_data_stream.py",
        must_contain=("Data Stream",),
    ),
    ExerciseExpectation(
        "module-03-collections", "ex6/ft_data_alchemist.py",
        must_contain=("Data Alchemist",),
    ),

    # Module 04
    ExerciseExpectation(
        "module-04-fileio", "ex3/ft_vault_security.py",
        must_contain=("Cyber Archives Security",),
    ),
]


def pytest_generate_tests(metafunc):  # type: ignore[no-untyped-def]
    if "case" in metafunc.fixturenames:
        metafunc.parametrize(
            "case", CASES, ids=[f"{c.module.split('-')[1]}/{c.path}" for c in CASES]
        )


def test_exercise(case: ExerciseExpectation) -> None:
    assert_expectation(case, "exercises")
