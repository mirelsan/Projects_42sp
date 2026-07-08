def main() -> None:

    class Plant:
        def __init__(self, name: str, height: float, age: int):
            self.name = name
            self.height = height
            self.age = age

        def show(self) -> None:
            print(f"Created: {self.name}: {self.height}cm, {self.age} days old")

        def grow(self) -> None:
            self.height += 1

    p1 = Plant("Rose", 25.0, 30)
    p2 = Plant("Sunflower", 80, 45)
    p3 = Plant("Cactus", 15, 120)
    p4 = Plant("Mushrooms", 26, 5)
    p5 = Plant("Onions", 22, 40)

    print("=== Plant Factory Output ===")
    p1.show()
    p2.show()
    p3.show()
    p4.show()
    p5.show()


if __name__ == "__main__":
    main()
