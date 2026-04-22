"""Three design patterns in ~60 lines.

Run with:
    python3 01_patterns_tour.py
"""
import abc


# --- Pattern 1: Abstract Factory ---------------------------------------


class Button(abc.ABC):
    @abc.abstractmethod
    def click(self) -> str:
        ...


class _Linux(Button):
    def click(self) -> str:
        return "Linux button clicked."


class _Mac(Button):
    def click(self) -> str:
        return "Mac button clicked."


class ButtonFactory(abc.ABC):
    @abc.abstractmethod
    def make(self) -> Button:
        ...


class LinuxFactory(ButtonFactory):
    def make(self) -> Button:
        return _Linux()


class MacFactory(ButtonFactory):
    def make(self) -> Button:
        return _Mac()


# --- Pattern 2: Mixin (capability) -------------------------------------


class Loggable:
    def log(self, msg: str) -> str:
        return f"[LOG] {msg}"


class NotifyingButton(_Linux, Loggable):
    def click(self) -> str:
        return self.log(super().click())


# --- Pattern 3: Strategy -----------------------------------------------


class SortStrategy(abc.ABC):
    @abc.abstractmethod
    def sort(self, data: list[int]) -> list[int]:
        ...


class Ascending(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        return sorted(data)


class Descending(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        return sorted(data, reverse=True)


def sort_with(values: list[int], strategy: SortStrategy) -> list[int]:
    return strategy.sort(values)


def main() -> None:
    print("=== Factory ===")
    for factory in (LinuxFactory(), MacFactory()):
        print(factory.make().click())

    print()
    print("=== Mixin ===")
    print(NotifyingButton().click())

    print()
    print("=== Strategy ===")
    data = [3, 1, 4, 1, 5, 9, 2]
    print("asc  ->", sort_with(data, Ascending()))
    print("desc ->", sort_with(data, Descending()))


if __name__ == "__main__":
    main()
