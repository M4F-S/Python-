def validate_ingredients(ingredients: str) -> str:
    # Lazy import breaks the potential light_spellbook <-> light_validator
    # cycle at import time: by the time this function runs, both modules
    # are fully initialised.
    from .light_spellbook import light_spell_allowed_ingredients

    allowed = light_spell_allowed_ingredients()
    tokens = ingredients.lower().replace(",", " ").split()
    if any(token in allowed for token in tokens):
        return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
