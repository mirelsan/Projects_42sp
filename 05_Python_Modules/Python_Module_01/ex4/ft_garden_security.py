def main() -> None:

    class Plant:
        def __init__(self, name: str, height: float, age: int) -> None:
            self.name = name
            self._validate_and_set_height(height)
            self._validate_and_set_age(age)

        def _validate_and_set_height(self, value: float) -> bool:
            if value < 0:
                return False
            self._height = value
            return True

        def _validate_and_set_age(self, value: int) -> bool:
            if value < 0:
                return False
            self._age = value
            return True

        def show(self) -> None:
            print(
                f"Plant created: {self.name}: {self._height}cm, {self._age} days old")

        def report(self) -> None:
            print(
                f"Current state: {self.name}: {self._height}cm, {self._age} days old")

        def get_height(self) -> float:
            return self._height

        def set_height(self, value: float) -> None:
            if self._validate_and_set_height(value):
                print("Height updated")
            else:
                print(f"{self.name}: Error, height can't be negative")
                print("Height update rejected")

        def get_age(self) -> int:
            return self ._age

        def set_age(self, value: int) -> None:
            if self._validate_and_set_age(value):
                print("Age updated")
            else:
                print(f"{self.name}: Error, age can't be negative")
                print("Age update rejected")

    print("=== Garden Security System ===")
    p1 = Plant("Rose", 15.0, 10)
    p1.show()
    p1.set_height(25.0)
    p1.set_age(30)
    p1.set_height(-5)
    p1.set_age(-3)
    p1.report()


if __name__ == "__main__":
    main()
