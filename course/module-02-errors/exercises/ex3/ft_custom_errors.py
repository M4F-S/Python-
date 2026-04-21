# Exercise 3 — ft_custom_errors
# Authorized: print()
#
# Define:
#   class GardenError(Exception): default msg "Unknown garden error"
#   class PlantError(GardenError): default msg "Unknown plant error"
#   class WaterError(GardenError): default msg "Unknown water error"
#
# Show raising each, catching each, and catching both via GardenError.


class GardenError(Exception):
    pass


class PlantError(GardenError):
    pass


class WaterError(GardenError):
    pass


if __name__ == "__main__":
    pass
