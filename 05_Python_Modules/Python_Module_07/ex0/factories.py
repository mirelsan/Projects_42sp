from abc import ABC, abstractmethod
from .creatures import Creature

class CreatureFactory(ABC):
    
    @abstractmethod
    def creature_base(self) -> Creature:
        pass

    def create_evolved(self) -> Creature:
        pass


class FlameFactory(CreateFactory):
    def creature_base(self) -> Creature:
        Flameling()
    
    def creature_evolved(self) -> Creature:
        Pyrodon()

class AquaFactory(CreateFactory):
    def creature_base(self) -> Creature:
        Aquabub()

    def creature_evolved(self) -> Creature:    
        Torragon()