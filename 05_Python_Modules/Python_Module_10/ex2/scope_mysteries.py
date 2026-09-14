from colections.abc import Any, Callable


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
    return accumulate

def enchantment_factory(enchantment_type: str) -> Callable:
    def apply_enchantment(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"
    return apply_enchantment

def memory_vault() -> dict[str, Callable]:
    storage: dic[str, Any] = {}

    def storage(key: str, value: Any) -> None:
        storage[key] = value
    
    def recall(key: str) -> Any:
        if key in storage:
            return storage[key]
        return "Memory not found"
    return {"store": store, "recall": recall}
