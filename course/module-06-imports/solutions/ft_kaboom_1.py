if __name__ == "__main__":
    print("=== Kaboom 1 ===")
    print("Access to alchemy/grimoire/dark_spellbook.py directly")
    print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")
    # Intentional top-level import that blows up due to the circular
    # dependency between dark_spellbook and dark_validator.
    from alchemy.grimoire.dark_spellbook import dark_spell_record  # noqa: F401
