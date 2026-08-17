from alchemy import elements


def main() -> None:
    print("=== Alembic 5 ===")
    print("Accessing the alchemy module using 'from alchemy import ...'")
    print("Testing create_air: ", end="")
    air = elements.create_air()
    print(air)


if __name__ == "__main__":
    main()
