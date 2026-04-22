class Plant:
    def __init__(self, name: str, height: float = 0.0, age: int = 0) -> None:
        self._name = name
        self._height = 0.0
        self._age = 0
        self.set_height(height)
        self.set_age(age)

    def get_height(self) -> float:
        return self._height

    def set_height(self, value: float) -> None:
        if value < 0:
            print(f"{self._name}: Error, height can't be negative")
            return
        self._height = float(value)

    def get_age(self) -> int:
        return self._age

    def set_age(self, value: int) -> None:
        if value < 0:
            print(f"{self._name}: Error, age can't be negative")
            return
        self._age = int(value)

    def show(self) -> None:
        print(f"{self._name}: {round(self._height, 1)}cm, "
              f"{self._age} days old")


if __name__ == "__main__":
    print("=== Garden Security System ===")
    rose = Plant("Rose", 15.0, 10)
    print("Plant created:", end=" ")
    rose.show()
    print()

    rose.set_height(25)
    print(f"Height updated: {round(rose.get_height())}cm")
    rose.set_age(30)
    print(f"Age updated: {rose.get_age()} days")
    print()

    rose.set_height(-5)
    print("Height update rejected")
    rose.set_age(-5)
    print("Age update rejected")
    print()

    print("Current state:", end=" ")
    rose.show()
