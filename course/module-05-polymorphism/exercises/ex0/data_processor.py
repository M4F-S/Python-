"""Exercise 0: Data Processor.

Build the abstract DataProcessor(ABC) base class along with three concrete
subclasses: NumericProcessor, TextProcessor, LogProcessor.

Required:
- DataProcessor(ABC) with:
    @abstractmethod validate(self, data: Any) -> bool
    @abstractmethod ingest(self, data: Any) -> None
    output(self) -> tuple[int, str]  (concrete)
- NumericProcessor: accepts int | float | list[int | float]
- TextProcessor:    accepts str | list[str]
- LogProcessor:     accepts dict[str, str] | list[dict[str, str]]

Authorized imports: typing, abc.

Implement the classes below and add a test harness under
`if __name__ == "__main__":` that reproduces the expected output shown in
the lesson / subject PDF.
"""
from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    # TODO: add shared state, e.g. an internal buffer and a rank counter.

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...

    def output(self) -> tuple[int, str]:
        # TODO: pop the oldest (rank, value) pair and return it.
        raise NotImplementedError


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        # TODO
        raise NotImplementedError

    def ingest(self, data: int | float | list[int | float]) -> None:
        # TODO
        raise NotImplementedError


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        # TODO
        raise NotImplementedError

    def ingest(self, data: str | list[str]) -> None:
        # TODO
        raise NotImplementedError


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        # TODO
        raise NotImplementedError

    def ingest(
        self,
        data: dict[str, str] | list[dict[str, str]],
    ) -> None:
        # TODO
        raise NotImplementedError


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")
    # TODO: reproduce the expected output from the subject PDF.
