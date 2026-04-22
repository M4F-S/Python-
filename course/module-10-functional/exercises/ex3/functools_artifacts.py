"""Exercise 3 - Ancient Library.

Authorized: functools, operator.
"""
from collections.abc import Callable
from functools import lru_cache, partial, reduce, singledispatch
from typing import Any

import operator  # noqa: F401


def spell_reducer(spells: list[int], operation: str) -> int:
    # TODO: map "add"/"multiply"/"max"/"min" onto operator / builtins,
    #       then reduce. Empty -> 0. Unknown op -> raise ValueError.
    raise NotImplementedError


def partial_enchanter(
    base_enchantment: Callable[[int, str, str], str],
) -> dict[str, Callable[[str], str]]:
    # TODO: use functools.partial to build 3 specialized variants with
    #       power=50 and a fixed element.
    raise NotImplementedError


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    # TODO: classic recursive fib. lru_cache makes it fast.
    raise NotImplementedError


def spell_dispatcher() -> Callable[[Any], str]:
    # TODO: singledispatch with int/str/list/Any branches.
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: exercise each artifact and print cache_info() for fib.
    pass
