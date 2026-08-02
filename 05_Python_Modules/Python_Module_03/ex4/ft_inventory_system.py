import sys


def parse_inventory(args: list[str]) -> dict[str, int]:
    inventory: dict[str, int] = {}
    for arg in args:
        parts = arg.split(":")
        if len(parts) != 2:
            print(f"Error - invalid parameter '{arg}'")
            continue
        name, qty_str = parts
        if name in inventory:
            print(f"Redundant item '{name}' - discarding")
            continue
        try:
            inventory[name] = int(qty_str)
        except ValueError as e:
            print(f"Quantity error for '{name}': {e}")
    return inventory


def main() -> None:
    print("=== Inventory System Analysis ===")

    inventory = parse_inventory(sys.argv[1:])
    print(f"Got inventory: {inventory}")

    if not inventory:
        return

    items = list(inventory.keys())
    print(f"Item list: {items}")

    total = sum(inventory.values())
    print(f"Total quantity of the {len(items)} items: {total}")

    for name, qty in inventory.items():
        percentage = round(qty / total * 100, 1)
        print(f"Item {name} represents {percentage}%")

    most = max(inventory, key=lambda item: inventory[item])
    least = min(inventory, key=lambda item: inventory[item])
    print(f"Item most abundant: {most} with quantity {inventory[most]}")
    print(f"Item least abundant: {least} with quantity {inventory[least]}")

    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
