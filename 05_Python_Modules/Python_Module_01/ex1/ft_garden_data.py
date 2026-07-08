def main():

    class Plant:
        def __init__(self, name, height, age):
            self.name = name
            self.height = height
            self.age = age

        def show(self):
            print(f"{self.name}: {self.height}cm, {self.age} days old")

    p1 = Plant("Rose", 25, 30)
    p2 = Plant("Sunflower", 80, 45)
    p3 = Plant("Cactus", 15, 120)

    print("=== Garden Plant Registry ===")
    p1.show()
    p2.show()
    p3.show()


if __name__ == "__main__":
    main()
