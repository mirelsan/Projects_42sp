from .dark_validator import validate_dark_ingredients


DARK_ALLOWED: list[str] = ["bats", "frogs", "arsenic", "eyeball"]


def dark_spell_allowed_ingredients() -> list[str]:
    return DARK_ALLOWED


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    result: str = validate_ingredients(ingredients)
    if "VALID" in result:
        return f"Spell recorded: {spell_name} ({result})"
    return f"Spell rejected: {spell_name} ({result})"
