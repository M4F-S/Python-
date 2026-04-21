from .light_validator import validate_ingredients


def light_spell_allowed_ingredients() -> list[str]:
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    status = validate_ingredients(ingredients)
    verb = "recorded" if status.endswith("VALID") else "rejected"
    return f"Spell {verb}: {spell_name} ({status})"
