"""Part IV - dark magic validator (intentionally broken).

Top-level circular import: we grab a name from dark_spellbook while
dark_spellbook is still being initialised. That's the kaboom.
"""
from .dark_spellbook import dark_spell_allowed_ingredients  # noqa: F401


def validate_ingredients(ingredients: str) -> str:
    # Unreachable in practice, because the import above will fail first.
    raise NotImplementedError
