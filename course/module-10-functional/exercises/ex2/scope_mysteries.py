"""Exercise 2 - Memory Depths.

Authorized: nonlocal (no global!).
"""
from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable[[], int]:
    # TODO: closure counting calls, starting at 1.
    #       Two independent counters must have independent state.
    raise NotImplementedError


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    # TODO: closure accumulating power from initial_power.
    raise NotImplementedError


def enchantment_factory(
    enchantment_type: str,
) -> Callable[[str], str]:
    # TODO: return a function that prefixes item names.
    raise NotImplementedError


def memory_vault() -> dict[str, Callable[..., Any]]:
    # TODO: private vault with 'store' and 'recall' closures.
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: demo each closure.
    pass
