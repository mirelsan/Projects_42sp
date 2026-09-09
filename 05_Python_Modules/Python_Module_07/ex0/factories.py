from abc import ABC, abstractmethod
from .creatures import Creature, Flameling, Pyrodon, Aquabub, Torragon


class CreatureFactory(ABC):

    @abstractmethod
    def creature_base(self) -> Creature:
        pass

    @abstractmethod
    def creature_evolved(self) -> Creature:
        pass


class FlameFactory(CreatureFactory):
    def creature_base(self) -> Creature:
        return Flameling()

    def creature_evolved(self) -> Creature:
        return Pyrodon()


class AquaFactory(CreatureFactory):
    def creature_base(self) -> Creature:
        return Aquabub()

    def creature_evolved(self) -> Creature:
        return Torragon()
