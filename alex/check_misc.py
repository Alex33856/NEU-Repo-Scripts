import json

from alex.utils import BasePath, check_for_item

miscPath = BasePath / "constants" / "misc.json"

with open(miscPath, "r") as f:
    talismanUpgrades = json.load(f)["talisman_upgrades"]


def Main():
    for key in talismanUpgrades:
        if not check_for_item(key):
            print(f"P: {key} does not exist!")

        currentGroupContained = set()
        for child in talismanUpgrades[key]:
            if child in currentGroupContained:
                print(f"C: {child} already exists in {key}!")

            if not check_for_item(child):
                print(f"C of {key}: {child} does not exist!")
            currentGroupContained.add(child)


if __name__ == "__main__":
    Main()
