from abc import ABC, abstractmethod

from .creatures import (
    Creature,
    _Aquabub,
    _Flameling,
    _Pyrodon,
    _Torragon,
)


class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature:
        ...

    @abstractmethod
    def create_evolved(self) -> Creature:
        ...


class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return _Flameling()

    def create_evolved(self) -> Creature:
        return _Pyrodon()


class AquaFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return _Aquabub()

    def create_evolved(self) -> Creature:
        return _Torragon()
