import operator
from collections.abc import Callable
from functools import lru_cache, partial, reduce, singledispatch
from typing import Any


_OPS: dict[str, Callable[[int, int], int]] = {
    "add": operator.add,
    "multiply": operator.mul,
    "max": max,
    "min": min,
}


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0
    if operation not in _OPS:
        raise ValueError(f"Unknown operation: {operation!r}")
    return reduce(_OPS[operation], spells)


def _base_enchantment(power: int, element: str, target: str) -> str:
    return f"{element.title()} spell hits {target} for {power} damage"


def partial_enchanter(
    base_enchantment: Callable[[int, str, str], str],
) -> dict[str, Callable[[str], str]]:
    return {
        "fire": partial(base_enchantment, 50, "fire"),
        "ice": partial(base_enchantment, 50, "ice"),
        "lightning": partial(base_enchantment, 50, "lightning"),
    }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @singledispatch
    def cast(arg: Any) -> str:
        return "Unknown spell type"

    @cast.register
    def _(arg: int) -> str:
        return f"{arg} damage"

    @cast.register
    def _(arg: str) -> str:
        return arg

    @cast.register
    def _(arg: list) -> str:
        return f"{len(arg)} spells"

    return cast


if __name__ == "__main__":
    print("Testing spell reducer...")
    powers = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(powers, 'add')}")
    print(f"Product: {spell_reducer(powers, 'multiply')}")
    print(f"Max: {spell_reducer(powers, 'max')}")
    print(f"Min: {spell_reducer(powers, 'min')}")
    print(f"Empty: {spell_reducer([], 'add')}")

    print()
    print("Testing partial enchanter...")
    shortcuts = partial_enchanter(_base_enchantment)
    print(shortcuts["fire"]("Goblin"))
    print(shortcuts["ice"]("Troll"))
    print(shortcuts["lightning"]("Dragon"))

    print()
    print("Testing memoized fibonacci...")
    for n in (0, 1, 10, 15):
        print(f"Fib({n}): {memoized_fibonacci(n)}")
    info = memoized_fibonacci.cache_info()
    print(f"cache: hits={info.hits}, misses={info.misses}")

    print()
    print("Testing spell dispatcher...")
    cast = spell_dispatcher()
    print(f"Damage spell: {cast(42)}")
    print(f"Enchantment: {cast('fireball')}")
    print(f"Multi-cast: {cast(['heal', 'shield', 'haste'])}")
    print(cast({"weird": True}))
