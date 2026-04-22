from abc import ABC, abstractmethod

from ex0.creatures import Creature


class StrategyError(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        ...

    @abstractmethod
    def act(self, creature: Creature) -> list[str]:
        ...


# TODO: NormalStrategy (valid for any creature)
# TODO: AggressiveStrategy (valid for TransformCapability creatures)
# TODO: DefensiveStrategy (valid for HealCapability creatures)
# Raise StrategyError in act() when is_valid is False.
