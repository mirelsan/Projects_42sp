import alchemy

def main() -> None:
    print("=== Alembic 4 ===")
    print("Accessing the alchemy module using 'import alchemy'")
    print("Testing create_air: ", end="")
    air = alchemy.create_air()
    print(air)

    print("Now show that not all functions can be reached")
    print("This will raise an exception!")
    print("Testing the hidden create_earth: ", end="")
    earth = alchemy.create_earth()
    print(earth)


if __name__ "__main__":
    main()
