from ex0 import CreatureFactory
from ex1 import (
    HealingCreatureFactory, 
    TransformCreatureFactory,
    HealCapability,
    TransformCapability,
)   


def test_healing_capability(factory: CreatureFactory) -> None:
    print("Testing Creature with healing capability")
    base = factory.create_evolved()
    evolved = factory.create_evolved()


def test_transform_capability(factory1: CreatureFactory) -> None:
    print("Testing Creature with transform capability")


def main() -> None:
    try:
        healing_factory = HealingCreatureFactory()
        transform_factory = TransformCreatureFactory()

        test_healing_capability(healing_factory)
        test_transform_capability(transform_factory)


    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()