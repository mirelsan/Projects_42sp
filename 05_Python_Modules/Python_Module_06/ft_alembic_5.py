from alchemy import elements
print("=== Alembic 5 ===")
print("Accessing the alchemy module using 'from alchemy import ...'")
print("Testing create_air: ", end="")
air = elements.create_air()
print(air)
