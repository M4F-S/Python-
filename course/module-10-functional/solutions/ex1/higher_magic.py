from collections.abc import Callable
from typing import Any


def spell_combiner(
    spell1: Callable[..., Any],
    spell2: Callable[..., Any],
) -> Callable[..., tuple[Any, Any]]:
    def combined(*args: Any, **kwargs: Any) -> tuple[Any, Any]:
        return (spell1(*args, **kwargs), spell2(*args, **kwargs))
    return combined


def power_amplifier(
    base_spell: Callable[[str, int], str],
    multiplier: int,
) -> Callable[[str, int], str]:
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified


def conditional_caster(
    condition: Callable[..., bool],
    spell: Callable[..., Any],
) -> Callable[..., Any]:
    def casted(*args: Any, **kwargs: Any) -> Any:
        if condition(*args, **kwargs):
            return spell(*args, **kwargs)
        return "Spell fizzled"
    return casted


def spell_sequence(
    spells: list[Callable[..., Any]],
) -> Callable[..., list[Any]]:
    def run(*args: Any, **kwargs: Any) -> list[Any]:
        return [s(*args, **kwargs) for s in spells]
    return run


def heal(target: str, power: int) -> str:
    return f"Heals {target}"


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target}"


def extract_power(_target: str, power: int) -> int:
    return power


if __name__ == "__main__":
    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    a, b = combined("Dragon", 10)
    print(f"Combined spell result: {a}, {b}")

    print()
    print("Testing power amplifier...")
    mega = power_amplifier(extract_power, 3)
    print(f"Original: {extract_power('Dragon', 10)}, "
          f"Amplified: {mega('Dragon', 10)}")

    print()
    print("Testing conditional caster...")
    only_strong = conditional_caster(
        lambda target, power: power >= 20,
        fireball,
    )
    print(f"power=25 -> {only_strong('Dragon', 25)}")
    print(f"power=10 -> {only_strong('Dragon', 10)}")

    print()
    print("Testing spell sequence...")
    barrage = spell_sequence([fireball, heal])
    for line in barrage("Dragon", 10):
        print(f"  - {line}")

    print()
    print("Note: Callable comes from collections.abc (PEP 585).")
    print(f"callable(fireball) -> {callable(fireball)}")
