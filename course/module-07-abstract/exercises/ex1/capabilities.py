from abc import ABC, abstractmethod
from typing import Any


class HealCapability(ABC):
    @abstractmethod
    def heal(self, target: Any = None) -> str:
        ...


class TransformCapability(ABC):
    def __init__(self) -> None:
        # TODO: persistent state (transformed or not)
        pass

    @abstractmethod
    def transform(self) -> str:
        ...

    @abstractmethod
    def revert(self) -> str:
        ...
