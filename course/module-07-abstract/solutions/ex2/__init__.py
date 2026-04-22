"""DataDeck ex2 - battle strategies."""
from .strategies import AggressiveStrategy as AggressiveStrategy
from .strategies import BattleStrategy as BattleStrategy
from .strategies import DefensiveStrategy as DefensiveStrategy
from .strategies import NormalStrategy as NormalStrategy
from .strategies import StrategyError as StrategyError

__all__ = [
    "AggressiveStrategy",
    "BattleStrategy",
    "DefensiveStrategy",
    "NormalStrategy",
    "StrategyError",
]
