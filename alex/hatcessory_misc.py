import json
from copy import deepcopy

from alex.utils import getAllItems, get_lore_for_file, ItemsPath, ConstantsPath

miscPath = ConstantsPath / "misc.json"

order = ["PARTY_HAT_CRAB", "PARTY_HAT_CRAB_ANIMATED", "PARTY_HAT_SLOTH",
         "BALLOON_HAT_2024", "BALLOON_HAT_2025", "CAKE_HAT_2026"]

color = ["AQUA", "BLACK", "GREEN", "LIME", "ORANGE", "PINK", "PURPLE", "RED", "YELLOW", ""]

emoji = ["CHEEKY", "COOL", "CUTE", "DERP", "FLUSHED", "GRUMPY", "HAPPY", "REGULAR", "SHOCK", "TEARS"]


def sort_function(value) -> int:
    baseIndex = -1
    for i, l in enumerate(order):
        if value.startswith(l):
            baseIndex = (i + 1)
            if value.endswith("_ANIMATED"):
                baseIndex += 1
            break
    for i, l in enumerate(color):
        if l in value:
            return baseIndex * len(color) + i
    for i, l in enumerate(emoji):
        if l in value:
            return baseIndex * len(color) + i
    return 0


def getRawHatcessories() -> list[str]:
    hatcessories = []
    for file in getAllItems():
        lore = get_lore_for_file(file)
        if lore is None:
            continue
        for line in lore:
            if line.endswith("HATCESSORY"):
                item = str(file.relative_to(ItemsPath)).replace(".json", "")
                hatcessories.append(item)
    return hatcessories


def getHatcessories() -> list[str]:
    hatcessories = ['BALLOON_HAT_2024_AQUA', 'BALLOON_HAT_2024_BLACK', 'BALLOON_HAT_2024_GREEN',
                    'BALLOON_HAT_2024_LIME', 'BALLOON_HAT_2024_ORANGE', 'BALLOON_HAT_2024_PINK',
                    'BALLOON_HAT_2024_PURPLE', 'BALLOON_HAT_2024_RED', 'BALLOON_HAT_2024_YELLOW',
                    'BALLOON_HAT_2025_AQUA', 'BALLOON_HAT_2025_BLACK', 'BALLOON_HAT_2025_GREEN',
                    'BALLOON_HAT_2025_LIME', 'BALLOON_HAT_2025_ORANGE', 'BALLOON_HAT_2025_PINK',
                    'BALLOON_HAT_2025_PURPLE', 'BALLOON_HAT_2025_RED', 'BALLOON_HAT_2025_YELLOW', 'CAKE_HAT_2026_AQUA',
                    'CAKE_HAT_2026_BLACK', 'CAKE_HAT_2026_GREEN', 'CAKE_HAT_2026_LIME', 'CAKE_HAT_2026_ORANGE',
                    'CAKE_HAT_2026_PINK', 'CAKE_HAT_2026_PURPLE', 'CAKE_HAT_2026_RED', 'CAKE_HAT_2026_YELLOW',
                    'PARTY_HAT_CRAB_AQUA', 'PARTY_HAT_CRAB_AQUA_ANIMATED', 'PARTY_HAT_CRAB_BLACK',
                    'PARTY_HAT_CRAB_BLACK_ANIMATED', 'PARTY_HAT_CRAB_GREEN', 'PARTY_HAT_CRAB_GREEN_ANIMATED',
                    'PARTY_HAT_CRAB_LIME', 'PARTY_HAT_CRAB_LIME_ANIMATED', 'PARTY_HAT_CRAB_ORANGE',
                    'PARTY_HAT_CRAB_ORANGE_ANIMATED', 'PARTY_HAT_CRAB_PINK', 'PARTY_HAT_CRAB_PINK_ANIMATED',
                    'PARTY_HAT_CRAB_PURPLE', 'PARTY_HAT_CRAB_PURPLE_ANIMATED', 'PARTY_HAT_CRAB_RED',
                    'PARTY_HAT_CRAB_RED_ANIMATED', 'PARTY_HAT_CRAB_YELLOW', 'PARTY_HAT_CRAB_YELLOW_ANIMATED',
                    'PARTY_HAT_SLOTH_CHEEKY', 'PARTY_HAT_SLOTH_COOL', 'PARTY_HAT_SLOTH_CUTE', 'PARTY_HAT_SLOTH_DERP',
                    'PARTY_HAT_SLOTH_FLUSHED', 'PARTY_HAT_SLOTH_GRUMPY', 'PARTY_HAT_SLOTH_HAPPY',
                    'PARTY_HAT_SLOTH_REGULAR', 'PARTY_HAT_SLOTH_SHOCK', 'PARTY_HAT_SLOTH_TEARS']
    for k in hatcessories:
        print(k, sort_function(k))
    hatcessories.sort(key=sort_function)
    print(hatcessories)
    return hatcessories


def readMisc() -> dict:
    with open(miscPath, encoding="utf-8") as f:
        misc = json.load(f)
    return misc


def writeMisc(misc: dict):
    with open(miscPath, "w", encoding="utf-8") as f:
        json.dump(misc, f, indent=2)


def update_talisman_upgrades(existing: dict[str, list[str]], hatcessories: list[str]) -> dict[str, list[str]]:
    for hatcessory in hatcessories:
        existing[hatcessory] = deepcopy(hatcessories)
        existing[hatcessory].remove(hatcessory)


def Main():
    hatcessories = getHatcessories()
    misc = readMisc()
    update_talisman_upgrades(misc["talisman_upgrades"], hatcessories)
    writeMisc(misc)


if __name__ == "__main__":
    Main()
