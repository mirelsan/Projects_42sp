import functools
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0

    ops: dict[str, Callable[[int, int], int]] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,  # Bult-in max function
        "min": min,  # Bult-in min function
    }

    if operation not in ops:
        raise ValueError(f"Unknown operation: {operation}")

    result: int = functools.reduce(ops[operation], spells)
    return result


def partial_enchanter(
    base_enchantment: Callable[..., str]
) -> dict[str, Callable[..., str]]:
    elements = ["fire", "frost", "arcane"]
    return {
        element: functools.partial(base_enchantment, 50, element)
        for element in elements
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @functools.singledispatch
    def cast(spell: Any) -> str:
        return "Unknown spell type"

    @cast.register
    def _(spell: int) -> str:
        return f"Damage spell: {spell} damage"

    @cast.register
    def _(spell: str) -> str:
        return f"Enchantment: {spell}"

    @cast.register
    def _(spell: list) -> str:
        return f"Multi-cast: {len(spell)} spells"

    return cast


def main() -> None:

    print("Testing spell reducer...")
    spells = [10, 20, 30, 40]

    print(f"Sum: {spell_reducer(spells, 'add')}")
    print(f"Product: {spell_reducer(spells, 'multiply')}")

    print("Testing memoized fibonacci...")
    print(f"Fib(0): {memoized_fibonacci(0)}")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")

    print("Testing spell dispatcher...")
    dispatch = spell_dispatcher()

    print(dispatch(42))
    print(dispatch("fireball"))
    print(dispatch(["spell1", "spell2", "spell3"]))

    print(dispatch(3.14))

    def base_spell(power: int, element: str, target: str) -> str:
        return f"Casting {element} on {target} with {power} power"
    enchanters = partial_enchanter(base_spell)
    fire_spell = enchanters["fire"]
    print(fire_spell("Dragon"))


if __name__ == "__main__":
    main()
