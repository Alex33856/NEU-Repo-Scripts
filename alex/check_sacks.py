import json

from alex.utils import ConstantsPath, ItemsPath

sacksPath = ConstantsPath.joinpath("sacks.json")
with open(sacksPath, "r") as f:
    sacksData = json.load(f)["sacks"]


def item_exists(itemId: str) -> bool:
    return ItemsPath.joinpath(f"{itemId}.json").exists()


def check_sack(name: str, sack: dict):
    item = sack["item"]
    contents = sack["contents"]

    if not item_exists(item):
        print(f"{name}'s item {item} does not exist.")
        return False

    for contentItem in contents:
        if not item_exists(contentItem):
            print(f"{name}'s item {contentItem} does not exist.")
            return False
    return True


def check_all_sacks():
    for sack in sacksData:
        if not check_sack(sack, sacksData[sack]):
            print(f"There is an issue with {sack} sack.")


if __name__ == "__main__":
    check_all_sacks()
