def main():

    class Plant:
        def __init__(self, name, height, age, tax):
            self.name = name
            self.height = height
            self.age_days = age
            self.tax = tax

        def grow(self):
            self.height = self.height + self.tax
            self.height = round(self.height, 2)

        def age(self):
            self.age_days = self.age_days + 1

    print("=== Garden Plant Growth ===")

    p1 = Plant("Rose", 25.0, 30, 1.5)
    p2 = Plant("Cactus", 15, 120, 0.2)

    print(f"{p1.name}: {p1.height}cm, {p1.age_days} days old")
    h = p1.height
    i = 0
    while i < 7:
        i += 1
        print(f"=== Day {i} ===")
        p1.grow()
        p1.age()
        print(f"{p1.name}: {p1.height}cm, {p1.age_days} days old")
    print(f"Growth this week: {round(p1.height - h, 2)}cm")

    print(f"{p2.name}: {p2.height}cm, {p2.age_days} days old")
    y = p2.height
    j = 0
    while j < 7:
        j += 1
        print(f"=== Day {j} ===")
        p2.grow()
        p2.age()
        print(f"{p2.name}: {p2.height}cm, {p2.age_days} days old")
    print(f"Growth this week: {round(p2.height - y, 2)}cm")


if __name__ == "__main__":
    main()
