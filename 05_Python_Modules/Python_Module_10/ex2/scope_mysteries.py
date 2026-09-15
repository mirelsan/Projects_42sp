from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable[[], int]:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total_power = initial_power

    def acumulate(power: int) -> int:
        nonlocal total_power
        total_power += power
        return total_power
    return acumulate


def enchantment_factory(enchantment_type: str) -> Callable:
    def apply_enchantment(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"
    return apply_enchantment


def memory_vault() -> dict[str, Callable]:
    storage: dict[str, Any] = {}

    def store(key: str, value: Any) -> None:
        storage[key] = value

    def recall(key: str) -> Any:
        if key in storage:
            return storage[key]
        return "Memory not found"
    return {"store": store, "recall": recall}


def main() -> None:
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()

    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")

    print(f"counter_b call 1: {counter_b()}")

    print("\nTesting spell accumulator...")
    accumulator = spell_accumulator(100)
    print(f"Base 100, add 20: {accumulator(20)}")
    print(f"Base 100, add 30: {accumulator(30)}")

    print("\nTesting enchantment factory...")

    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")

    print(flaming("Sword"))
    print(frozen("Shield"))

    print("\nTesting memory vault...")
    vault = memory_vault()
    store = vault["store"]
    recall = vault["recall"]

    store("secret", 42)
    print("Store 'secret': 42")
    print(f"Recall 'secret': {recall('secret')}")
    print(f"Recall 'unknown': {recall('unknown')}")


if __name__ == "__main__":
    main()
