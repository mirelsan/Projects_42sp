from ex0 import CreatureFactory, FlameFactory, AquaFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
    InvalidStrategyError
)


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    for i in range(len(opponents)):
        for j in range(i + 1, len(opponents)):
            fac1, strat1 = opponents[i]
            fac2, strat2 = opponents[j]

            fighter1 = fac1.create_base()
            fighter2 = fac2.create_base()

            print("* Battle *")
            print(fighter1.describe())
            print("vs.")
            print(fighter2.describe())
            print("now fight!")

            try:
                strat1.act(fighter1)
                strat2.act(fighter2)
            except InvalidStrategyError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


def main() -> None:
    try:
        flame = FlameFactory()
        aqua = AquaFactory()
        healing = HealingCreatureFactory()