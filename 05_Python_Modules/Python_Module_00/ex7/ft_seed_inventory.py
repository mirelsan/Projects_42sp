def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    if unit == "packets":
        print(seed_type.capitalize() + " seeds: " + str(quantity) + " packets available")
    elif unit == "grams":
        print(seed_type.capitalize() + " seeds: " + str(quantity) + " grams total")  
    elif unit == "area":
        print(seed_type.capitalize() + " seeds: covers" + str(quantity) + " square meters")