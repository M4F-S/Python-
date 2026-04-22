from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable[[], int]:
    count = 0

    def tick() -> int:
        nonlocal count
        count += 1
        return count

    return tick


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total = initial_power

    def add(amount: int) -> int:
        nonlocal total
        total += amount
        return total

    return add


def enchantment_factory(
    enchantment_type: str,
) -> Callable[[str], str]:
    def apply(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return apply


def memory_vault() -> dict[str, Callable[..., Any]]:
    vault: dict[str, Any] = {}

    def store(key: str, value: Any) -> None:
        vault[key] = value

    def recall(key: str) -> Any:
        return vault.get(key, "Memory not found")

    return {"store": store, "recall": recall}


if __name__ == "__main__":
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print()
    print("Testing spell accumulator...")
    accum = spell_accumulator(100)
    print(f"Base 100, add 20: {accum(20)}")
    print(f"Base 100, add 30: {accum(30)}")

    print()
    print("Testing enchantment factory...")
    flame = enchantment_factory("Flaming")
    frost = enchantment_factory("Frozen")
    print(flame("Sword"))
    print(frost("Shield"))

    print()
    print("Testing memory vault...")
    vault = memory_vault()
    vault["store"]("secret", 42)
    print(f"Store 'secret' = 42")
    print(f"Recall 'secret': {vault['recall']('secret')}")
    print(f"Recall 'unknown': {vault['recall']('unknown')}")
