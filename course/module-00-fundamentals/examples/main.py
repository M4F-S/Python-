"""Generic test harness.

Copy this file INTO the exercise folder you want to test
(e.g. exercises/ex2/main.py), then run: python3 main.py

It looks for a module with the expected name next to it and calls
the function. Works for ex0 through ex7.
"""
import importlib
import sys

# (module_name, function_name, call_args_or_None)
# If call_args_or_None is None, call with ().
# ex7 takes positional args — we demo three inputs.
TESTS = [
    ("ft_hello_garden",             "ft_hello_garden",             ()),
    ("ft_garden_name",              "ft_garden_name",              ()),
    ("ft_plot_area",                "ft_plot_area",                ()),
    ("ft_harvest_total",            "ft_harvest_total",            ()),
    ("ft_plant_age",                "ft_plant_age",                ()),
    ("ft_water_reminder",           "ft_water_reminder",           ()),
    ("ft_count_harvest_iterative",  "ft_count_harvest_iterative",  ()),
    ("ft_count_harvest_recursive",  "ft_count_harvest_recursive",  ()),
]


def _try(mod_name: str, func_name: str, args: tuple) -> None:
    try:
        mod = importlib.import_module(mod_name)
    except ModuleNotFoundError:
        return
    func = getattr(mod, func_name, None)
    if func is None:
        print(f"[skip] {mod_name}.{func_name} not found")
        return
    print(f"── {mod_name}.{func_name}{args} ──")
    func(*args)
    print()


def main() -> None:
    if len(sys.argv) > 1:
        wanted = sys.argv[1]
        for mod, fn, args in TESTS:
            if mod == wanted or fn == wanted:
                _try(mod, fn, args)
        return
    for mod, fn, args in TESTS:
        _try(mod, fn, args)

    # ex7 demo — only runs if the module exists
    try:
        inv = importlib.import_module("ft_seed_inventory")
        print("── ft_seed_inventory demo ──")
        inv.ft_seed_inventory("tomato", 15, "packets")
        inv.ft_seed_inventory("carrot", 8, "grams")
        inv.ft_seed_inventory("lettuce", 12, "area")
        inv.ft_seed_inventory("bean", 3, "liters")
    except ModuleNotFoundError:
        pass


if __name__ == "__main__":
    main()
