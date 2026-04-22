import random


ACHIEVEMENTS: list[str] = [
    "Boss Slayer", "Speed Runner", "Collector Supreme",
    "Master Explorer", "Strategist", "Crafting Genius",
    "Untouchable", "Unstoppable", "Sharp Mind",
    "Treasure Hunter", "World Savior", "First Steps",
    "Survivor", "Hidden Path Finder",
]

PLAYERS: list[str] = ["Alice", "Bob", "Charlie", "Dylan"]


def gen_player_achievements(pool: list[str]) -> set[str]:
    count = random.randint(4, len(pool) - 2)
    return set(random.sample(pool, count))


if __name__ == "__main__":
    print("=== Achievement Tracker System ===")
    print()

    books: dict[str, set[str]] = {}
    for name in PLAYERS:
        books[name] = gen_player_achievements(ACHIEVEMENTS)
        print(f"Player {name}: {books[name]}")
        print()

    all_sets = list(books.values())

    distinct: set[str] = set()
    for s in all_sets:
        distinct = distinct.union(s)
    print(f"All distinct achievements: {distinct}")
    print()

    common: set[str] = set(all_sets[0])
    for s in all_sets[1:]:
        common = common.intersection(s)
    print(f"Common achievements: {common}")
    print()

    for name in PLAYERS:
        others: set[str] = set()
        for other_name in PLAYERS:
            if other_name != name:
                others = others.union(books[other_name])
        print(f"Only {name} has: {books[name].difference(others)}")
    print()

    full = set(ACHIEVEMENTS)
    for name in PLAYERS:
        print(f"{name} is missing: {full.difference(books[name])}")
        print()
