import random


ALL_ACHIEVEMENTS = [
    "Crafting Genius", "Strategist", "World Savior", "Speed Runner",
    "Survivor", "Master Explorer", "Treasure Hunter", "Unstoppable",
    "First Steps", "Collector Supreme", "Untouchable", "Sharp Mind",
    "Boss Slayer", "Hidden Path Finder",
]


def gen_player_achievements() -> set[str]:
    count = random.randint(3, 9)
    return set(random.sample(ALL_ACHIEVEMENTS, count))


def main() -> None:
    print("=== Achievement Tracker System ===\n")

    players: dict[str, set[str]] = {
        "Alice": gen_player_achievements(),
        "Bob": gen_player_achievements(),
        "Charlie": gen_player_achievements(),
        "Dylan": gen_player_achievements(),
    }

    for name, achievements in players.items():
        print(f"Player {name}: {achievements}")

    all_distinct: set[str] = set().union(*players.values())
    print(f"\nAll distinct achievements: {all_distinct}")

    common: set[str] = set.intersection(*players.values())
    print(f"Common achievements: {common}")
    print()

    for name, achievements in players.items():
        others = [s for other_name, s in players.items() if other_name != name]
        only_this = achievements.difference(*others)
        print(f"Only {name} has: {only_this}")

    print()

    for name, achievements in players.items():
        missing = all_distinct.difference(achievements)
        print(f"{name} is missing: {missing}")


if __name__ == "__main__":
    main()
