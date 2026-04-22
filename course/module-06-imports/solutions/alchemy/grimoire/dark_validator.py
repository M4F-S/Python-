# Intentionally top-level circular import: dark_validator imports from
# dark_spellbook, which is still being initialised when this module is
# loaded. Result: ImportError as soon as dark_spellbook is touched.
from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    allowed = dark_spell_allowed_ingredients()
    tokens = ingredients.lower().replace(",", " ").split()
    if any(token in allowed for token in tokens):
        return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
