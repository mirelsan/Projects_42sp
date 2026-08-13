import alchemy.elements

def main() -> None:
    print("=== Alembic 2 ===")
    print("Accessing alchemy/elements.py using 'import ...' structure")
    print("Testing create_earth: ", end="")
    earth = alchemy.elements.create_earth()
    print(earth)


if __name__ == "__main__":
    main()
