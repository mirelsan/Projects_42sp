from elements import create_water


def main() -> None:
    print("=== Alembic 1 ===")
    print("Using: 'from ... import ...' structure to access elements.py")
    print("Testing create_water: ", end="")
    water = create_water()
    print(water)


if __name__ == "__main__":
    main()
