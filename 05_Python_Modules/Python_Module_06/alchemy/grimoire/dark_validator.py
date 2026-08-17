from .dark_spellbook import dark_spell_allowed_ingredients


def validate_dark_ingredients(ingredients: str) -> str:
    from .dark_spellbook import dark_spell_allowed_ingredients

    allowed: list[str] = dark_spell_allowed_ingredients()
    for ingredient in allowed:
        if ingredient.lower() in ingredients.lower():
            return f"{ingredients} - VALID"

    return f"{ingredients} - INVALID"
