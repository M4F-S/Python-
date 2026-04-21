from .dark_validator import validate_ingredients


def dark_spell_allowed_ingredients() -> list[str]:
    return ["bats", "frogs", "arsenic", "eyeball"]


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    status = validate_ingredients(ingredients)
    verb = "recorded" if status.endswith("VALID") else "rejected"
    return f"Spell {verb}: {spell_name} ({status})"
