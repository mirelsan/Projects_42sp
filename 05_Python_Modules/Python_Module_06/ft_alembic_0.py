import elements

def main() -> None:
    print("=== Alembic 0 ===")
    print("Using: 'import ...' structure to access elements.py")
    print("Testing create_fire: ", end="")
    fire = elements.create_fire()
    print(fire)


if __name__ == "__main__":
    main()
