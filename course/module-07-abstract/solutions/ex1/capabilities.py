from abc import ABC, abstractmethod
from typing import Any


class HealCapability(ABC):
    @abstractmethod
    def heal(self, target: Any = None) -> str:
        ...


class TransformCapability(ABC):
    def __init__(self) -> None:
        self._transformed: bool = False

    @abstractmethod
    def transform(self) -> str:
        ...

    @abstractmethod
    def revert(self) -> str:
        ...
