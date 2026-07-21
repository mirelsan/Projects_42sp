def main() -> None:

    class Plant:
        def __init__(self, name: str, height: float, age: int) -> None:
            self.name = name
            self._height = height
            self._age = age

        def show(self) -> None:
            print(f"{self.name}: {self._height}cm, {self._age} days old")
            
        @staticmethod
        def is_older_than_a_year(age: int) -> bool:
            return age > 365

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
                print("[asking the rose to grow and bloom]")
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

    class Seed(Flower):
        def __init__(
            self,
            name: str,
            height: float,
            age: int,
            petal_color: str,
        ) -> None:
            super().__init__(name, height, age)
            self.petal_color = petal_color
            self.bloomed = False

        def show(self) -> None:
            super().show()
            print(f"Color: {self.petal_color}")

        def bloom(self) -> None:
            if not self.bloomed:
                print(f"{self.name} has not bloomed yet")
                print("[make sunflower grow, age and bloom]")
                self.bloomed = True
            else:
                print(f"{self.name} is blooming beautifully!")

    print("=== Garden statistics ===")
    print("=== Check year-old")

    print()
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
    print("=== Seed")
    tomato = Seed("Sunflower", 5.0, 10, "April")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    tomato.grow(20)
    tomato.show()


if __name__ == "__main__":
    main()