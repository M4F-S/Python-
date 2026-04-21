import random


if __name__ == "__main__":
    print("=== Game Data Alchemist ===")
    print()

    players: list[str] = ["Alice", "bob", "Charlie", "dylan",
                          "Emma", "Gregory", "john", "kevin", "Liam"]
    print(f"Initial list of players: {players}")
    print()

    all_capitalized: list[str] = [name.capitalize() for name in players]
    print(f"New list with all names capitalized: {all_capitalized}")
    print()

    already_capitalized: list[str] = [
        name for name in players if name == name.capitalize()
    ]
    print(f"New list of capitalized names only: {already_capitalized}")
    print()

    scores: dict[str, int] = {
        name: random.randint(0, 1000) for name in all_capitalized
    }
    print(f"Score dict: {scores}")
    print()

    average = round(sum(scores.values()) / len(scores), 2)
    print(f"Score average is {average}")

    high_scores: dict[str, int] = {
        n: s for n, s in scores.items() if s > average
    }
    print(f"High scores: {high_scores}")
