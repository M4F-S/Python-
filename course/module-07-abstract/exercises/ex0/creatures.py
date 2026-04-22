"""Creature + concrete types.

Tip: prefix concrete classes with _ to keep them package-private, and
omit them from __init__.py so callers can only reach them via factories.
"""
from abc import ABC, abstractmethod


class Creature(ABC):
    # TODO: __init__ takes name + type_.

    @abstractmethod
    def attack(self) -> str:
        ...

    def describe(self) -> str:
        # TODO: "<name> is a <type_> type Creature"
        raise NotImplementedError


# TODO: _Flameling, _Pyrodon, _Aquabub, _Torragon.
