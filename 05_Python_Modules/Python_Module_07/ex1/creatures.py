from ex0 import Creature
from .capabilities import HealCapability, TransformCapability


class Sproutling(Creature, HealCapability):
    def __init__(self) -> None:
        super().__init__("Sproutling", "Grass")

    def attack(self) -> str:
        return f"{self.name} uses Vine Whip!"

    def heal(self) -> str:
        return f"{self.name} heals itself for a small amount"


class Bloomelle(Creature, HealCapability):
    def __init__(self) -> None:
        super().__init__("Bloomelle","Grass/Fairy")

    def attack(self) -> str:
        return f"{self.name} uses Petal Dance!"

    def heal(self) -> str:
        return f"{self.name} heals itself and others for a large amount"


class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        super().__init__("Shiftling", "Normal")
        self.is_transformed = False

    
    def transform(self) -> str:
        self.is_transformed = True
        return f"{self.name} shifts into a sharper form!"
    
    def revert(self) -> str:
        self.is_transformed = False
    
    def attack(self) -> str:
        if self.is_transformed
            return f"{self.name} performs a boosted strike!"
        return f"{self.name} attacks normally"


class Morphagon(Creature, TransformCapability):
    def __init__(self):
        super().__init__("Morphagon", "Normal/Dragon")
        self.is_transformed = False
    
    def transform(self) -> str:
        self.is_transform = True
        return f"{self.name} morphs into a dragonic battle form!"

    def revert(self) -> str:
        self.is_transformed = False
    
    def attack(self) -> str:
        if self.is_transformed
            return f"{self.name} unleashes a devastating morph strike!"
        return f"{self.name} attacks normally."
