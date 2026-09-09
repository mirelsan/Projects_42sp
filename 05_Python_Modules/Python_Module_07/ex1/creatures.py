from ex0 import Creature
from .capabilities import HealCapability, TransformCapability

class Sprouling(Creature, HealCapability):



class Bloomelle(Creature, HealCapability):



class Shiftling(Creature, TransformCapability):
    def __init__(self):
        Creature.__init__(self, name="Shiftling", type_="Normal")
        TransformCapability.__init__(self)
    
    def transform(self) -> str:
        self.is_transformed = True
        return f"{self.name} shifts into a sharper form!"
    
    def revert(self) -> str:
        self.is_transformed = True
    
    def attack(self) -> str:
        if self.is_transformed
            return f"{self.name} performs a boosted strike!"
        return f"{self.name} attacks normally"


class Morphagon(Creature, TransformCapability):
    def __init__(self):
        Creature.__init__(self, name="Morphagon", type_="Normal/Dragon")
        TransformCapability.__init__(self)
    
    def transform(self) -> str:
        self.is_transform = True
        return f"{self.name} morphs into a dragonic battle form!"

    def revert(self) -> str:
        self.is_transformed = True
    
    def attack(self) -> str:
        if self.is_transformed
            return f"{self.name} unleashes a devastating morph strike!"
        return f"{self.name} attacks normally."
