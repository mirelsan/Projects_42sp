def main() -> None:

    class Plant:
        def __init__(self, name: str, height: float, age: int) -> None:
            self.name = name
            self._height = height
            self._age = age

        def show(self) -> None:
            print(f"{self.name}: {self._height}cm, {self._age} days old")

    class Flower(Plant):
        def __init__(
            self, name: str,
            height: float,
            age: int,
            petal_color: str,
        ) -> None:
            super().__init__(name, height, age)
            self.petal_color = petal_color
            self.bloomed = False

        def bloom(self) -> None:
            if not self.bloomed:
                print(f"{self.name} has not bloomed yet")
                print("[asking the rose to bloom]")
                self.bloomed = True
            else:
                print(f"{self.name} is blooming beautifully!")

        def show(self) -> None:
            super().show()
            print(f"Color: {self.petal_color}")

    class Tree(Plant):
        def __init__(
            self,
            name: str,
            height: float,
            age: int,
            trunk_diameter: float,
        ) -> None:
            super().__init__(name, height, age)
            self.trunk_diameter = trunk_diameter
            self.shading = False

        def show(self) -> None:
            super().show()
            print(f"Trunk diameter: {self.trunk_diameter}cm")
            print("[asking the oak to produce shade]")

        def produce_shade(self) -> None:
            if not self.shading:
                self.shading = True
            print(f"Tree {self.name} now produces a shade of"
                  f"{self._height}cm long and {self.trunk_diameter}cm wide")

    class Vegetable(Plant):
        def __init__(
            self,
            name: str,
            height: float,
            age: int,
            harvest_season: str,
        ) -> None:
            super().__init__(name, height, age)
            self.harvest_season = harvest_season
            self.nutritional_value = 0

        def show(self) -> None:
            super().show()
            print(f"Harvest season: {self.harvest_season}")
            print(f"Nutritional value: {self.nutritional_value}")

        def grow(self, days: int) -> None:
            self._height += days * 2.1
            self._age += days
            self.nutritional_value += days

    print("=== Garden Plant Types ===")
    print("=== Flower")
    color = Flower("Rose", 15.0, 10, "red")
    color.show()
    color.bloom()
    color.bloom()
    print()
    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    oak.produce_shade()
    print()
    print("=== Vegetable")
    tomato = Vegetable("Tomato", 5.0, 10, "April")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    tomato.grow(20)
    tomato.show()


if __name__ == "__main__":
    main()
