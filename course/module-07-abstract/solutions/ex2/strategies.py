from abc import ABC, abstractmethod

from ex0.creatures import Creature
from ex1.capabilities import HealCapability, TransformCapability


class StrategyError(Exception):
    pass


class BattleStrategy(ABC):
    name: str = "strategy"

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        ...

    @abstractmethod
    def act(self, creature: Creature) -> list[str]:
        ...


class NormalStrategy(BattleStrategy):
    name = "normal"

    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> list[str]:
        return [creature.attack()]


class AggressiveStrategy(BattleStrategy):
    name = "aggressive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise StrategyError(
                f"Invalid Creature '{creature.name}' "
                f"for this {self.name} strategy"
            )
        assert isinstance(creature, TransformCapability)
        return [
            creature.transform(),
            creature.attack(),
            creature.revert(),
        ]


class DefensiveStrategy(BattleStrategy):
    name = "defensive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise StrategyError(
                f"Invalid Creature '{creature.name}' "
                f"for this {self.name} strategy"
            )
        assert isinstance(creature, HealCapability)
        return [creature.attack(), creature.heal()]
