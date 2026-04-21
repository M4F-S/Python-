# Exercise 4 — ft_finally_block
# Authorized: print(), str.capitalize()
#
# Bring PlantError in (copy it from ex3). water_plant(name) raises
# PlantError if the plant name is not capitalized (name != name.capitalize()).
# Otherwise prints "Watering <Name>: [OK]".
#
# test_watering_system():
#   prints "Opening watering system"
#   try: water several plants; catch PlantError, print caught, return
#   finally: print "Closing watering system"
# Demonstrate with a valid batch and a batch containing "lettuce".


class GardenError(Exception):
    pass


class PlantError(GardenError):
    pass


def water_plant(plant_name: str) -> None:
    pass


def test_watering_system(plants: list[str]) -> None:
    pass


if __name__ == "__main__":
    pass
