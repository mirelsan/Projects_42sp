def main() -> None:

    class Plant:
        def __init__(self, name: str, height: float, age: int):
            self.name = name
            self.height = height
            self.age = age

    @property
    def height        