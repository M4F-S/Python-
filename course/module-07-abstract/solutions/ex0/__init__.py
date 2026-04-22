"""DataDeck ex0 - expose only abstract Creature and factories."""
from .creatures import Creature as Creature
from .factories import AquaFactory as AquaFactory
from .factories import CreatureFactory as CreatureFactory
from .factories import FlameFactory as FlameFactory

__all__ = [
    "AquaFactory",
    "Creature",
    "CreatureFactory",
    "FlameFactory",
]
