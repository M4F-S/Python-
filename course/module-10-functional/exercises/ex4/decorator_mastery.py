"""Exercise 4 - Master's Tower.

Authorized: functools.wraps, staticmethod.
"""
import time
from collections.abc import Callable
from functools import wraps
from typing import Any


def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    # TODO: decorator that prints "Casting <name>..." before, then
    # "Spell completed in X.XXX seconds" after, using perf_counter.
    raise NotImplementedError


def power_validator(
    min_power: int,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    # TODO: decorator factory. The wrapped function's first arg must be
    # `power`. If power < min_power, return "Insufficient power for this
    # spell"; otherwise call the function.
    raise NotImplementedError


def retry_spell(
    max_attempts: int,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    # TODO: decorator factory. On exception, print "Spell failed,
    # retrying... (attempt n/max)". After max_attempts failures,
    # return "Spell casting failed after <n> attempts".
    raise NotImplementedError


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        # TODO: >= 3 chars, letters/spaces only.
        raise NotImplementedError

    def cast_spell(self, spell_name: str, power: int) -> str:
        # TODO: delegate to an inner helper decorated with
        # @power_validator(min_power=10).
        raise NotImplementedError


if __name__ == "__main__":
    # TODO: exercise each decorator and MageGuild.
    pass
