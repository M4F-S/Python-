class Plant:
    _growth_rate: float = 1.0

    class _Stats:
        def __init__(self) -> None:
            self._grow = 0
            self._age = 0
            self._show = 0

        def display(self) -> None:
            print(f"Stats: {self._grow} grow, "
                  f"{self._age} age, {self._show} show")

    def __init__(self, name: str, height: float = 0.0, age: int = 0) -> None:
        self._name = name
        self._height = 0.0
        self._age = 0
        self._stats = self._make_stats()
        self.set_height(height)
        self.set_age(age)

    def _make_stats(self) -> "Plant._Stats":
        return Plant._Stats()

    @staticmethod
    def is_older_than_one_year(age_days: int) -> bool:
        return age_days > 365

    @classmethod
    def anonymous(cls) -> "Plant":
        return cls("Unknown plant")

    def get_name(self) -> str:
        return self._name

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

    def grow(self) -> None:
        self._stats._grow += 1
        self._height += self._growth_rate

    def age(self) -> None:
        self._stats._age += 1
        self._age += 1

    def show(self) -> None:
        self._stats._show += 1
        print(f"{self._name}: {round(self._height, 1)}cm, "
              f"{self._age} days old")

    def stats(self) -> "Plant._Stats":
        return self._stats


class Flower(Plant):
    def __init__(self, name: str, color: str = "unknown",
                 height: float = 0.0, age: int = 0) -> None:
        super().__init__(name, height, age)
        self._color = color
        self._blooming = False

    def bloom(self) -> None:
        self._blooming = True

    def show(self) -> None:
        super().show()
        print(f"Color: {self._color}")
        if self._blooming:
            print(f"{self._name} is blooming beautifully!")
        else:
            print(f"{self._name} has not bloomed yet")


class Seed(Flower):
    def __init__(self, name: str, color: str = "unknown",
                 height: float = 0.0, age: int = 0,
                 seeds: int = 0) -> None:
        super().__init__(name, color, height, age)
        self._seeds = 0
        self._pending_seeds = seeds

    def bloom(self) -> None:
        super().bloom()
        self._seeds = self._pending_seeds

    def show(self) -> None:
        super().show()
        print(f"Seeds: {self._seeds}")


class Tree(Plant):
    _growth_rate: float = 0.5

    class _TreeStats(Plant._Stats):
        def __init__(self) -> None:
            super().__init__()
            self._shade = 0

        def display(self) -> None:
            super().display()
            print(f"{self._shade} shade")

    def _make_stats(self) -> "Plant._Stats":
        return Tree._TreeStats()

    def __init__(self, name: str, trunk_diameter: float = 0.0,
                 height: float = 0.0, age: int = 0) -> None:
        super().__init__(name, height, age)
        self._trunk_diameter = float(trunk_diameter)

    def produce_shade(self) -> None:
        assert isinstance(self._stats, Tree._TreeStats)
        self._stats._shade += 1
        print(f"Tree {self._name} now produces a shade of "
              f"{round(self._height, 1)}cm long "
              f"and {round(self._trunk_diameter, 1)}cm wide.")

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {round(self._trunk_diameter, 1)}cm")


def display_stats(plant: "Plant") -> None:
    plant.stats().display()


if __name__ == "__main__":
    print("=== Garden statistics ===")

    print("=== Check year-old")
    for d in (30, 400):
        answer = Plant.is_older_than_one_year(d)
        print(f"Is {d} days more than a year? -> {answer}")
    print()

    print("=== Flower")
    rose = Flower("Rose", "red", 15.0, 10)
    rose.show()
    print("[statistics for Rose]")
    display_stats(rose)
    print("[asking the rose to grow and bloom]")
    for _ in range(8):
        rose.grow()
    rose.bloom()
    rose.show()
    print("[statistics for Rose]")
    display_stats(rose)
    print()

    print("=== Tree")
    oak = Tree("Oak", 5.0, 200.0, 365)
    oak.show()
    print("[statistics for Oak]")
    display_stats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print("[statistics for Oak]")
    display_stats(oak)
    print()

    print("=== Seed")
    sunflower = Seed("Sunflower", "yellow", 80.0, 45, seeds=42)
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    for _ in range(30):
        sunflower.grow()
    for _ in range(20):
        sunflower.age()
    sunflower.bloom()
    sunflower.show()
    print("[statistics for Sunflower]")
    display_stats(sunflower)
    print()

    print("=== Anonymous")
    unknown = Plant.anonymous()
    unknown.show()
    print("[statistics for Unknown plant]")
    display_stats(unknown)
