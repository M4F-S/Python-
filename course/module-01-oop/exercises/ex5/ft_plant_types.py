# Exercise 5 — ft_plant_types
# Authorized: super(), print(), range(), round()
#
# Subclass Plant into Flower, Tree, Vegetable.
#   Flower    : color, bloom()
#   Tree      : trunk_diameter, produce_shade()
#   Vegetable : harvest_season, nutritional_value (starts at 0, grows with
#               grow()/age() calls)
# Each specialized show() must call super().show() and add its extras.


class Plant:
    pass


class Flower(Plant):
    pass


class Tree(Plant):
    pass


class Vegetable(Plant):
    pass


if __name__ == "__main__":
    pass
