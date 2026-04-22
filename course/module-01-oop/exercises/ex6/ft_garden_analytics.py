# Exercise 6 — ft_garden_analytics
# Authorized: super(), print(), range(), round(), staticmethod(), classmethod()
#
# On top of ex5, add:
#   - Plant.is_older_than_one_year(age_days)    @staticmethod
#   - Plant.anonymous()                          @classmethod -> Plant
#   - Seed(Flower)                               holds seed count after bloom
#   - Plant._Stats nested class (grow, age, show counters). Encapsulated.
#   - Tree adds a shade counter (extended stats).
#   - Top-level function display_stats(plant)    works for any plant.


class Plant:
    pass


class Flower(Plant):
    pass


class Seed(Flower):
    pass


class Tree(Plant):
    pass


class Vegetable(Plant):
    pass


def display_stats(plant: "Plant") -> None:
    pass


if __name__ == "__main__":
    pass
