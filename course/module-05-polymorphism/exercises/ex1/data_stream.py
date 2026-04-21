"""Exercise 1: Polymorphic Processing of a Data Stream.

Extend Exercise 0 with a DataStream class. It must:
- register_processor(self, proc: DataProcessor) -> None
- process_stream(self, stream: list[typing.Any]) -> None
      Route each element to the first registered processor that
      validate()-s it. Otherwise print a "Can't process" error line.
- print_processors_stats(self) -> None
      Print a formatted statistics block. Match the subject example.

Authorized imports: typing, abc.
"""
from abc import ABC, abstractmethod
from typing import Any

# TODO: paste / re-implement DataProcessor, NumericProcessor,
# TextProcessor and LogProcessor from Exercise 0 here.


class DataStream:
    def __init__(self) -> None:
        # TODO
        raise NotImplementedError

    def register_processor(self, proc: "DataProcessor") -> None:
        # TODO
        raise NotImplementedError

    def process_stream(self, stream: list[Any]) -> None:
        # TODO
        raise NotImplementedError

    def print_processors_stats(self) -> None:
        # TODO
        raise NotImplementedError


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===")
    # TODO: reproduce the subject's scenario.
