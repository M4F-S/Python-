"""Part IV - dark magic spellbook.

This file INTENTIONALLY forms a circular import with dark_validator.py.
Keep the `from .dark_validator import validate_ingredients` at the
TOP of the module so it blows up on import. That's the whole point.
"""
from .dark_validator import validate_ingredients  # noqa: F401 intentional


def dark_spell_allowed_ingredients() -> list[str]:
    # TODO: return ["bats", "frogs", "arsenic", "eyeball"]
    raise NotImplementedError


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    # TODO
    raise NotImplementedError
