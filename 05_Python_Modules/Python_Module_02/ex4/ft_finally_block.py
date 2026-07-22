class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        self.message = message
        super().__init__(self.message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unkown plant error") -> None:
        self.message = message
        super().__init__(self.message)


def water_plant(plant_name: str) -> None:
    if plant_name == plant_name.capitalize():
        print(f"Watering {plant_name}: [OK]")
    else:
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")


def test_watering_system(plant_names: list[str]) -> None:
    print("Opening watering system")
    i = 0
    try:
        while i < len(plant_names):
            water_plant(plant_names[i])
            i += 1
    except PlantError as e:
        print(f"Caught PlantError: {e}")
        print("...ending tests and returning to main")
        return
    finally:
        print("Closing watering system")


def main() -> None:
    print("=== Garden Watering System ===")
    print()
    valid_plants = ["Tomato", "Lettuce", "Carrots"]
    invalid_plants = ["Tomato", "lettuce", "Carrots"]
    print("Testing valid plants...")
    test_watering_system(valid_plants)
    print("Testing invalid plants...")
    test_watering_system(invalid_plants)
    print("Cleanup always happens, even with errors!")


if __name__ == "__main__":
    main()
