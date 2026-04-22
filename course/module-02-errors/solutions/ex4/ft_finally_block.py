class GardenError(Exception):
    DEFAULT = "Unknown garden error"

    def __init__(self, message: str = "") -> None:
        super().__init__(message or self.DEFAULT)


class PlantError(GardenError):
    DEFAULT = "Unknown plant error"


def water_plant(plant_name: str) -> None:
    if plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"Watering {plant_name}: [OK]")


def test_watering_system(plants: list[str]) -> None:
    print("Opening watering system")
    try:
        for name in plants:
            water_plant(name)
    except PlantError as e:
        print(f"Caught PlantError: {e}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system")


if __name__ == "__main__":
    print("=== Garden Watering System ===")
    print()

    print("Testing valid plants...")
    test_watering_system(["Tomato", "Lettuce", "Carrots"])
    print()

    print("Testing invalid plants...")
    test_watering_system(["Tomato", "lettuce", "Carrots"])
    print()

    print("Cleanup always happens, even with errors!")
