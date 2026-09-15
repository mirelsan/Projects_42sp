from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined_wrapper(target: str, power: int) -> tuple[str, str]:
        result1 = spell1(target, power)
        result2 = spell2(target, power)
        return (result1, result2)
    return combined_wrapper


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified_wrapper(target: str, power: str) -> str:
        amplified_power = power * multiplier
        result: str = base_spell(target, amplified_power)
        return result
    return amplified_wrapper


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def wrapper_spell(target: str, power: int) -> str:
        if condition(target, power):
            result: str = spell(target, power)
            return result
        return "Spell fizzled"
    return wrapper_spell


def spell_sequence(spells: list[Callable]) -> Callable:
    def sequence_wrapper(target: str, power: int) -> list[str]:
        result = []
        for spell in spells:
            result.append(spell(target, power))
        return result
    return sequence_wrapper


def main() -> None:
    def fireball(target: str, power: int) -> str:
        return f"Fireball hits {target} for {power} damage"

    def heal(target: str, power: int) -> str:
        return f"Heal restores {target} for {power} HP"

    def is_enemy(target: str, power: int) -> bool:
        return target != "Ally"

    print("Testing spell combiner...")

    combined_spell = spell_combiner(fireball, heal)

    res1, res2 = combined_spell("Dragon", 10)
    print(f"Combined spell result: {res1}, {res2}")

    mega_fireball = power_amplifier(fireball, 3)
    print("\nTesting power amplifier...")
    print(mega_fireball("Dragon", 10))

    print("\nTesting conditional caster...")

    safe_fireball = conditional_caster(is_enemy, fireball)
    print(safe_fireball("Dragon", 15))
    print(safe_fireball("Ally", 15))

    print("\nTesting spell sequence...")
    sequence = spell_sequence([fireball, heal, fireball])
    results = sequence("Demon", 20)
    for res in results:
        print(res)


if __name__ == "__main__":
    main()
