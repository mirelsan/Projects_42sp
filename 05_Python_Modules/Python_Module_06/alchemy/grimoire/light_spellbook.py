from .light_validator import validate_ingredients


LIGHT_ALLOWED: list[str] = ["earth", "air", "fire", "water"]


def light_spell_allowed_ingredients() -> list[str]:
    return LIGHT_ALLOWED


def light_spell_record(spell_name: str, ingredients: str) -> str:
    result: str = validate_ingredients(ingredients)
    if "VALID" in result:
        return f"Spell recorded: {spell_name} ({result})"
    return f"Spell rejected: {spell_name} ({result})"
