def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda a: a["power"], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda m: m["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda s: f"* {s} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    if not mages:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}
    max_power = max(mages, key=lambda m: m["power"])["power"]
    min_power = min(mages, key=lambda m: m["power"])["power"]
    avg_power = round(
        sum(map(lambda m: m["power"], mages)) / len(mages),
        2,
    )
    return {
        "max_power": max_power,
        "min_power": min_power,
        "avg_power": avg_power,
    }


if __name__ == "__main__":
    artifacts = [
        {"name": "Crystal Orb", "power": 85, "type": "divination"},
        {"name": "Fire Staff", "power": 92, "type": "offense"},
        {"name": "Healing Wand", "power": 70, "type": "restoration"},
    ]
    mages = [
        {"name": "Alex", "power": 88, "element": "fire"},
        {"name": "Jordan", "power": 74, "element": "ice"},
        {"name": "Riley", "power": 95, "element": "lightning"},
        {"name": "Cadet", "power": 42, "element": "earth"},
    ]
    spells = ["fireball", "heal", "shield"]

    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    top = sorted_artifacts[0]
    second = sorted_artifacts[1]
    print(
        f"{top['name']} ({top['power']} power) comes before "
        f"{second['name']} ({second['power']} power)"
    )

    print()
    print("Testing power filter (min_power=80)...")
    strong = power_filter(mages, 80)
    for m in strong:
        print(f"  - {m['name']} ({m['power']})")

    print()
    print("Testing spell transformer...")
    print(" ".join(spell_transformer(spells)))

    print()
    print("Testing mage stats...")
    stats = mage_stats(mages)
    print(
        f"max={stats['max_power']} "
        f"min={stats['min_power']} "
        f"avg={stats['avg_power']}"
    )
