"""Part IV - light magic (no circular explosion).

light_spell_record validates the ingredients via light_validator, then
returns either a "Spell recorded: ..." or "Spell rejected: ..." string.
"""
# TODO: decide how to import from light_validator without creating a cycle.


def light_spell_allowed_ingredients() -> list[str]:
    # TODO: return ["earth", "air", "fire", "water"]
    raise NotImplementedError


def light_spell_record(spell_name: str, ingredients: str) -> str:
    # TODO
    raise NotImplementedError
