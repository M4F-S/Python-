class Plant:
    name: str = ""
    height: float = 0.0
    age: int = 0
    growth_rate: float = 0.8     # cm per day

    def show(self) -> None:
        print(f"{self.name}: {round(self.height, 1)}cm, {self.age} days old")

    def grow(self) -> None:
        self.height += self.growth_rate

    def age_one_day(self) -> None:
        self.age += 1


if __name__ == "__main__":
    print("=== Garden Plant Growth ===")
    rose = Plant()
    rose.name = "Rose"
    rose.height = 25.0
    rose.age = 30
    start_height = rose.height
    rose.show()

    for day in range(1, 8):
        rose.grow()
        rose.age_one_day()
        print(f"=== Day {day} ===")
        rose.show()

    print(f"Growth this week: {round(rose.height - start_height, 1)}cm")
