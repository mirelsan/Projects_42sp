from alchemy.elements import create_air


def main() -> None:
    print("=== Alembic 3 ===")
    print("Accessing alchemy/elements.py using"
          "'from ... import ...' structure"
          )
    print("Testing create_air: ", end="")
    air = create_air()
    print(air)


if __name__ == "__main__":
    main()
