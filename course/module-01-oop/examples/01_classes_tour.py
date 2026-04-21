"""Tour of Python classes for a C programmer.

Run:  python3 01_classes_tour.py
"""


class Point:
    """Like a struct + methods."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def show(self) -> None:
        print(f"Point({self.x}, {self.y})")

    def distance_to(self, other: "Point") -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5


class ColoredPoint(Point):
    """Inherits from Point, adds a color."""

    def __init__(self, x: float, y: float, color: str) -> None:
        super().__init__(x, y)
        self.color = color

    def show(self) -> None:
        super().show()
        print(f"  color: {self.color}")


class Vault:
    """Encapsulation via the _protected convention + getters/setters."""

    def __init__(self, balance: float = 0) -> None:
        self._balance = 0.0
        self.set_balance(balance)

    def get_balance(self) -> float:
        return self._balance

    def set_balance(self, value: float) -> None:
        if value < 0:
            print("Error: negative balance rejected")
            return
        self._balance = float(value)


class Counter:
    """Static and class methods."""

    _count = 0   # class variable shared by every instance

    def __init__(self) -> None:
        Counter._count += 1

    @staticmethod
    def describe() -> str:
        return "Counter keeps track of how many instances exist."

    @classmethod
    def total(cls) -> int:
        return cls._count


if __name__ == "__main__":
    p = Point(1, 2)
    q = ColoredPoint(4, 6, "red")
    p.show()
    q.show()
    print("distance:", p.distance_to(q))

    v = Vault(100)
    v.set_balance(-5)          # prints the error, keeps 100
    print("balance:", v.get_balance())

    Counter(); Counter(); Counter()
    print(Counter.describe())
    print("total instances:", Counter.total())
