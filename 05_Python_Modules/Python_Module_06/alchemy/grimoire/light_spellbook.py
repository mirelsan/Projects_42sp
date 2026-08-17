

LIGHT_ALLOWED: list[str] = ["earth", "air", "fire", "water"]

def light_spell_allowed_ingredients() -> str:
    return LIGHT_ALLOWED


def light_spell_record(spell_name: str, ingredients: str):
