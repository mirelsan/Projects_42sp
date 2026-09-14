import functools
import operator
from colections.abc import Any, Callable


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0

    ops = {
        "add": operator.add,
        "multiply": operator.mul
        "max": operator.max,
        "min": operator.min,
    }

    if operation not in ops:
        raise ValueError(f"Unknown operation: {operation}")

    return functools.reduce(ops[operation], spells)

def partial_enchanter(base_enchantment: Callable[..., str]) -> dict[str, Callable[...,str]]:
        elements = ["fire", "frest", "arcane"]
    return {
        element: functools.partial(base_enchantment, 50, element)
        for element in elements
    }

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
    def _(spell: str) -> str:
        return f"Mult-cast: {len(spell)} spells"
    return cast
    