from ex0 import CreatureFactory, FlameFactory, AquaFactory


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base_creature = factory.creature_base()
    evolved_creature = factory.creature_evolved()

    print(base_creature.describe())
    print(base_creature.attack())

    print(evolved_creature.describe())
    print(evolved_creature.attack())


def test_battle(factory1: CreatureFactory, factory2: CreatureFactory) -> None:
    print("Testing battle")
    fighter1 = factory1.creature_base()
    fighter2 = factory2.creature_base()

    print(fighter1.describe())
    print("vs.")
    print(fighter2.describe())
    print("fight!")

    print(fighter1.attack())
    print(fighter2.attack())


def main() -> None:
    try:
        flame_factory = FlameFactory()
        aqua_factory = AquaFactory()

        test_factory(flame_factory)
        test_factory(aqua_factory)

        test_battle(flame_factory, aqua_factory)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
