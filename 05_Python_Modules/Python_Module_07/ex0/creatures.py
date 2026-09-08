from abc import ABC, abstractmethod

class Creature(ABC) -> None:
    def __init__(self, name: str, creature_type: str) -> None:
        self.name = name
        self.type = creature_type

    @abstractmethod
    def attack(self) -> str:
        pass
    
    def describe(self) -> str:
        return f"{self.name} is a {self.type} Type Creature"
    

class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        return f"{self.name} uses Ember!"


class Pyrodon(Creature):
    def __init__(self) -> None:
        super().__init__("Pyrodon", "Fire/Flying")
    
    def attack(self) -> str:
        return f"{self.name} uses Flamethrower!"


class Aquabub(Creature):
    def __init__(self) -> None:
        super().__init__("Aquabub", "Water")
    
    def attack(self) -> None:
        return f"{self.name} uses Water Gun!"


class Torragon(Creature):
    def __init__(self) -> str:
        super().__init__("Torragon", "Water")

    def attack(self) -> None:
        return f"{self.name} uses Hydro Pump!"