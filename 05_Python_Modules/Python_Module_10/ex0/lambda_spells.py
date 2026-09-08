def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(
        artifacts, key=lambda artifact: artifact['power'], reverse=True
    )


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda mage: mage['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: f"* {spell} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    statistics: dict[str, int | float] = {}

    if not mages:
        statistics['max_power'] = 0
        statistics['min_power'] = 0
        statistics['avg_power'] = 0.0
        return statistics

    statistics['max_power'] = max(
        mages, key=lambda mage: mage['power']
    )['power']
    statistics['min_power'] = min(
        mages, key=lambda mage: mage['power']
    )['power']

    sum_powers = sum(map(lambda mage: mage['power'], mages))
    statistics['avg_power'] = round(sum_powers / len(mages), 2)

    return statistics


if __name__ == "__main__":

    artifacts_data = [
        {'name': 'Crystal', 'power': 85, 'type': 'Orb'},
        {'name': 'Fire Staff', 'power': 92, 'type': 'Staff'}
    ]

    spells_data = ["fireball", "heal", "shield"]

    mages_data = [
        {'name': 'Alex', 'power': 45, 'element': 'Water'},
        {'name': 'Jason', 'power': 86, 'element': 'Fire'},
        {'name': 'Clancy', 'power': 95, 'element': 'Earth'}
    ]

    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts_data)
    print(
        f"{sorted_artifacts[0]['name']} "
        f"({sorted_artifacts[0]['power']} power) "
        f"comes before {sorted_artifacts[1]['name']} "
        f"({sorted_artifacts[1]['power']} power)"
    )

    print("\nTesting spell transformer...")
    transformed = spell_transformer(spells_data)
    for spell in transformed:
        print(spell)

    print("\nTesting power filter (min_power = 80)...")
    strong_mages = power_filter(mages_data, 80)
    for mage in strong_mages:
        print(f"Found: {mage['name']} with {mage['power']} power")

    print("\nTesting mage stats...")
    stats = mage_stats(mages_data)
    print(f"Max Power: {stats['max_power']}")
    print(f"Min Power: {stats['min_power']}")
    print(f"Average Power: {stats['avg_power']}")
