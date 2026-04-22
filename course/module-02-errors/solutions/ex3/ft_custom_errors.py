class GardenError(Exception):
    DEFAULT = "Unknown garden error"

    def __init__(self, message: str = "") -> None:
        super().__init__(message or self.DEFAULT)


class PlantError(GardenError):
    DEFAULT = "Unknown plant error"


class WaterError(GardenError):
    DEFAULT = "Unknown water error"


def check_plant(name: str) -> None:
    raise PlantError(f"The {name} plant is wilting!")


def check_water(level: int) -> None:
    raise WaterError("Not enough water in the tank!")


def demo_catch_all() -> None:
    for func in (lambda: check_plant("tomato"),
                 lambda: check_water(0)):
        try:
            func()
        except GardenError as e:
            print(f"Caught GardenError: {e}")


if __name__ == "__main__":
    print("=== Custom Garden Errors Demo ===")
    print()

    print("Testing PlantError...")
    try:
        check_plant("tomato")
    except PlantError as e:
        print(f"Caught PlantError: {e}")
    print()

    print("Testing WaterError...")
    try:
        check_water(0)
    except WaterError as e:
        print(f"Caught WaterError: {e}")
    print()

    print("Testing catching all garden errors...")
    demo_catch_all()
    print()
    print("All custom error types work correctly!")
