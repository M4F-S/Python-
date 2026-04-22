from abc import ABC, abstractmethod

from .creatures import Creature


class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature:
        ...

    @abstractmethod
    def create_evolved(self) -> Creature:
        ...


# TODO: FlameFactory -> (_Flameling, _Pyrodon)
# TODO: AquaFactory  -> (_Aquabub, _Torragon)
