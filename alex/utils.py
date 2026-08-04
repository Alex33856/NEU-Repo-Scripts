import json
from os import listdir
from os.path import isfile
from pathlib import Path
from typing import Optional

import requests

with open("../path.txt", "r", encoding="UTF-8") as f:
    BasePath = Path(f.readline().strip())

ItemsPath = BasePath.joinpath("items")
OverlayPath = BasePath.joinpath("itemsOverlay")
ConstantsPath = BasePath.joinpath("constants")

rarityMap = [
    "COMMON",
    "UNCOMMON",
    "RARE",
    "EPIC",
    "LEGENDARY",
    "MYTHIC"
]


def getSNBTVersions() -> list[str]:
    versions = [entry.name for entry in OverlayPath.iterdir() if entry.is_dir()]
    versions.sort(reverse=True)
    return versions


def check_for_item(itemId) -> bool:
    path = ItemsPath / f"{itemId}.json"
    return path.exists()

def getAllItems() -> list[Path]:
    dirContents = listdir(ItemsPath)
    validFiles = []

    for path in dirContents:
        fullPath = ItemsPath.joinpath(path)
        if isfile(fullPath):
            validFiles.append(fullPath)

    return validFiles

def get_lore_for_file(path: Path) -> Optional[list[str]]:
    if not path.exists():
        return None

    with open(path, "r", encoding="UTF-8") as f:
        item = json.load(f)
    return item["lore"]

bazaar_products: Optional[list[str]] = None
def get_bazaar_products() -> list[str]:
    global bazaar_products
    if bazaar_products is None:
        bazaarData = requests.get("https://api.hypixel.net/v2/skyblock/bazaar").json()
        bazaar_products = products = bazaarData["products"].keys()
        return products
    return bazaar_products
