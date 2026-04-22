from ex0.creatures import Creature
from ex0.factories import CreatureFactory

from .creatures import _Bloomelle, _Morphagon, _Shiftling, _Sproutling


class HealingCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return _Sproutling()

    def create_evolved(self) -> Creature:
        return _Bloomelle()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return _Shiftling()

    def create_evolved(self) -> Creature:
        return _Morphagon()
