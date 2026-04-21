"""Exercise 2: Data Pipeline.

Extend Exercise 1 with an output pipeline plugged in via duck typing.

Required:
- ExportPlugin(typing.Protocol) with:
      def process_output(self, data: list[tuple[int, str]]) -> None: ...
- DataStream.output_pipeline(self, nb: int, plugin: ExportPlugin) -> None
      Consume up to nb items from every registered processor via output()
      and feed the resulting list to plugin.process_output() once per
      processor.
- At least two plugins, a CSV one and a JSON one. Build the CSV/JSON
  strings by hand - no csv / json imports.

Authorized imports: typing, abc.
"""
from abc import ABC, abstractmethod
from typing import Any, Protocol

# TODO: DataProcessor / NumericProcessor / TextProcessor / LogProcessor
# and DataStream from Exercise 1.


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        # TODO: print "CSV Output:" followed by a comma-joined line.
        raise NotImplementedError


class JSONPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        # TODO: print "JSON Output:" followed by a JSON-looking string
        #       built manually (no json import).
        raise NotImplementedError


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===")
    # TODO: reproduce the subject's scenario.
