"""Exercise-side tests for Module 00 (Fundamentals).

Module 00's 42 subject forbids `if __name__ == "__main__":` blocks, so
we load each file and call its function directly.
"""
from ._harness import FunctionExpectation, assert_function

MODULE = "module-00-fundamentals"

CASES = [
    FunctionExpectation(
        MODULE, "ex0/ft_hello_garden.py", "ft_hello_garden",
        must_contain=("Garden",),
    ),
    FunctionExpectation(
        MODULE, "ex1/ft_garden_name.py", "ft_garden_name",
        stdin="MyGarden\n",
        must_contain=("MyGarden", "Growing well!"),
    ),
    FunctionExpectation(
        MODULE, "ex2/ft_plot_area.py", "ft_plot_area",
        stdin="3\n4\n", must_contain=("12",),
    ),
    FunctionExpectation(
        MODULE, "ex3/ft_harvest_total.py", "ft_harvest_total",
        stdin="1\n2\n3\n", must_contain=("6",),
    ),
    FunctionExpectation(
        MODULE, "ex4/ft_plant_age.py", "ft_plant_age",
        stdin="90\n", must_contain=("ready to harvest",),
    ),
    FunctionExpectation(
        MODULE, "ex5/ft_water_reminder.py", "ft_water_reminder",
        stdin="5\n", must_contain=("Water",),
    ),
    FunctionExpectation(
        MODULE, "ex6/ft_count_harvest_iterative.py",
        "ft_count_harvest_iterative",
        stdin="3\n", must_contain=("Day 1", "Day 2", "Day 3", "Harvest time!"),
    ),
    FunctionExpectation(
        MODULE, "ex6/ft_count_harvest_recursive.py",
        "ft_count_harvest_recursive",
        stdin="3\n", must_contain=("Day 1", "Day 2", "Day 3", "Harvest time!"),
    ),
    FunctionExpectation(
        MODULE, "ex7/ft_seed_inventory.py", "ft_seed_inventory",
        args=("carrot", 5, "packets"),
        must_contain=("Carrot seeds: 5 packets available",),
    ),
]


def pytest_generate_tests(metafunc):  # type: ignore[no-untyped-def]
    if "case" in metafunc.fixturenames:
        metafunc.parametrize("case", CASES, ids=[c.path for c in CASES])


def test_exercise(case: FunctionExpectation) -> None:
    assert_function(case, "exercises")
