"""Exercise 1 - Higher Realm.

Authorized helpers: callable(), Callable.
Callable must come from collections.abc, not typing.
"""
from collections.abc import Callable
from typing import Any


def spell_combiner(
    spell1: Callable[..., Any],
    spell2: Callable[..., Any],
) -> Callable[..., tuple[Any, Any]]:
    # TODO: return a function that calls both and returns a tuple.
    raise NotImplementedError


def power_amplifier(
    base_spell: Callable[[str, int], str],
    multiplier: int,
) -> Callable[[str, int], str]:
    # TODO: return a function that multiplies power before delegating.
    raise NotImplementedError


def conditional_caster(
    condition: Callable[..., bool],
    spell: Callable[..., Any],
) -> Callable[..., Any]:
    # TODO: cast only if condition(*args) is True, else "Spell fizzled".
    raise NotImplementedError


def spell_sequence(
    spells: list[Callable[..., Any]],
) -> Callable[..., list[Any]]:
    # TODO: run every spell in order; return the list of results.
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: demo each higher-order function.
    pass
