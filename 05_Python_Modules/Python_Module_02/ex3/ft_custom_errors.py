
class GardenError(Exception):
    def __init__(self, message="Unknown garden error"):
        self.message = message
        super().__init__(self.message)


class PlantError(GardenError):
    def __init__(self, message="Unknown plant error"):
        self.message = message
        super().__init__(self.message)


class WaterError(GardenError):
    def __init__(self, message="Unknown water error"):
        self.message = message
        super().__init__(self.message)


def check_plant() -> None:
    raise PlantError("The tomato plant is wilting!")


def check_water() -> None:
    raise WaterError("Not enough water in the tank!")


def main() -> None:
    print("=== Custom Garden Errors Demo ===")
    print()

    print("Testing PlantError...")
    function = [check_plant]
    i = 0
    while i < len(function):
        try:
            function[i]()
        except PlantError as e:
            print(f"Caught PlantError: {e}")
            print()
        i += 1
    print("Testing WaterError...")
    function = [check_water]
    i = 0
    while i < len(function):
        try:
            function[i]()
        except WaterError as e:
            print(f"Caught WaterError: {e}")
            print()
        i += 1
    print("Testing catching all garden errors...")
    function = [check_plant, check_water]
    i = 0
    while i < len(function):
        try:
            function[i]()
        except GardenError as e:
            print(f"Caught GardenError: {e}")
        i += 1

    print()
    print("All custom error types work correctly!")


if __name__ == "__main__":
    main()
