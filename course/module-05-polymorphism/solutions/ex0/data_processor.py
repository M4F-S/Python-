from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._buffer: list[str] = []
        self._next_rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...

    def output(self) -> tuple[int, str]:
        if not self._buffer:
            raise IndexError("No data available for output")
        value = self._buffer.pop(0)
        rank = self._next_rank - len(self._buffer) - 1
        return (rank, value)

    def _store(self, value: str) -> None:
        self._buffer.append(value)
        self._next_rank += 1

    def total_processed(self) -> int:
        return self._next_rank

    def remaining(self) -> int:
        return len(self._buffer)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, bool):
            return False
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(
                not isinstance(x, bool) and isinstance(x, (int, float))
                for x in data
            )
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._store(str(item))
        else:
            self._store(str(data))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._store(item)
        else:
            self._store(data)


class LogProcessor(DataProcessor):
    @staticmethod
    def _is_log_dict(data: Any) -> bool:
        return (
            isinstance(data, dict)
            and all(isinstance(k, str) for k in data.keys())
            and all(isinstance(v, str) for v in data.values())
        )

    def validate(self, data: Any) -> bool:
        if self._is_log_dict(data):
            return True
        if isinstance(data, list):
            return all(self._is_log_dict(x) for x in data)
        return False

    def ingest(
        self,
        data: dict[str, str] | list[dict[str, str]],
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        entries: list[dict[str, str]]
        if isinstance(data, dict):
            entries = [data]
        else:
            entries = data
        for entry in entries:
            level = entry.get("log_level", "")
            message = entry.get("log_message", "")
            self._store(f"{level}: {message}")


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")
    print()

    print("Testing Numeric Processor...")
    num = NumericProcessor()
    print(f"Trying to validate input '42': {num.validate(42)}")
    print(f"Trying to validate input 'Hello': {num.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num.ingest("foo")  # type: ignore[arg-type]
    except ValueError as exc:
        print(f"Got exception: {exc}")
    payload = [1, 2, 3, 4, 5]
    print(f"Processing data: {payload}")
    num.ingest(payload)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = num.output()
        print(f"Numeric value {rank}: {value}")
    print()

    print("Testing Text Processor...")
    txt = TextProcessor()
    print(f"Trying to validate input '42': {txt.validate(42)}")
    words = ["Hello", "Nexus", "World"]
    print(f"Processing data: {words}")
    txt.ingest(words)
    print("Extracting 1 value...")
    rank, value = txt.output()
    print(f"Text value {rank}: {value}")
    print()

    print("Testing Log Processor...")
    log = LogProcessor()
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")
    logs = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"Processing data: {logs}")
    log.ingest(logs)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")
