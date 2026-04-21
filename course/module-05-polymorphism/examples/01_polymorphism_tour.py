"""A runnable tour of Python polymorphism.

Run with:
    python3 examples/01_polymorphism_tour.py
"""
import abc
import typing


# --- 1. Inheritance + method overriding ---------------------------------


class Animal:
    def speak(self) -> str:
        return "<silence>"


class Dog(Animal):
    def speak(self) -> str:
        return "woof"


class Cat(Animal):
    def speak(self) -> str:
        return "meow"


def describe(a: Animal) -> None:
    # No isinstance() check: dynamic dispatch picks the right speak().
    print(f"{type(a).__name__} says {a.speak()}")


# --- 2. Abstract Base Class ---------------------------------------------


class Shape(abc.ABC):
    @abc.abstractmethod
    def area(self) -> float:
        ...

    def describe(self) -> str:
        # Concrete method usable by every subclass.
        return f"{type(self).__name__} area={self.area():.2f}"


class Circle(Shape):
    def __init__(self, r: float) -> None:
        self.r = r

    def area(self) -> float:
        return 3.141592653589793 * self.r ** 2


class Square(Shape):
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side * self.side


# --- 3. Duck typing via Protocol ----------------------------------------


class SupportsArea(typing.Protocol):
    def area(self) -> float:
        ...


def biggest(items: list[SupportsArea]) -> SupportsArea:
    # Accepts anything with .area() - no inheritance required.
    return max(items, key=lambda x: x.area())


class Triangle:  # NOT inheriting Shape / SupportsArea
    def __init__(self, base: float, height: float) -> None:
        self.base = base
        self.height = height

    def area(self) -> float:
        return 0.5 * self.base * self.height


def main() -> None:
    print("=== 1. Classical overriding ===")
    for a in (Dog(), Cat(), Animal()):
        describe(a)

    print()
    print("=== 2. ABC refuses to instantiate the base class ===")
    try:
        Shape()  # type: ignore[abstract]
    except TypeError as exc:
        print(f"Shape() -> TypeError: {exc}")

    for s in (Circle(2.0), Square(3.0)):
        print(s.describe())

    print()
    print("=== 3. Protocol / duck typing ===")
    shapes: list[SupportsArea] = [Circle(1.0), Square(4.0), Triangle(3, 5)]
    winner = biggest(shapes)
    print(f"biggest is a {type(winner).__name__} "
          f"with area {winner.area()}")


if __name__ == "__main__":
    main()
