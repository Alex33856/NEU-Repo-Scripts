import json
from pathlib import Path

import requests

from alex.check_snbt import getSnbtFiles
from alex.nbt_utils import parse_nbt
from alex.utils import getSNBTVersions, ConstantsPath
from get_api_item_models import itemModels

files = []


def checkSnbt(path: Path):
    fileAndDir = str(path.relative_to(path.parent.parent))
    with open(path, "r", encoding="utf-8") as file:
        try:
            text = file.read()
            data = parse_nbt(text)
        except Exception as ex:
            print(f"Failed to read {fileAndDir}!")
            print(ex)
            return
    components = data["components"]
    itemModel = components.get("minecraft:item_model")
    itemId = components.get("minecraft:custom_data", {}).get("id")
    if itemId is None:
        return

    hypixelItemModel = itemModels.get(itemId)
    if hypixelItemModel is None:
        return

    if hypixelItemModel != itemModel:
        print(fileAndDir, " | ", itemId, " | ", f"{itemModel} vs {hypixelItemModel}")
        files.append(itemId)


def write_csv(fileName: str, items: list[str]):
    with open(fileName + ".csv", "w", encoding="utf-8") as file:
        file.write("\n".join(items))


def write_ssv(fileName: str, items: list[str]):
    with open(fileName + ".txt", "w", encoding="utf-8") as file:
        file.write(" ".join(items))


def filterBazaar(items: list[str]) -> tuple[list[str], list[str]]:
    inBazaar = set()

    bazaarStocksPath = ConstantsPath.joinpath("bazaarstocks.json")
    with open(bazaarStocksPath) as json_file:
        bazaarStocks = json.load(json_file)
        for item in bazaarStocks:
            inBazaar.add(item['id'])

    bazaarData = requests.get("https://api.hypixel.net/v2/skyblock/bazaar").json()
    products = bazaarData["products"].keys()
    inBazaar.update(products)

    bazaarable = []
    nonBazaarable = []
    for item in items:
        if item in inBazaar:
            bazaarable.append(item)
        else:
            nonBazaarable.append(item)

    return bazaarable, nonBazaarable


def Main():
    for version in getSNBTVersions():
        for file in getSnbtFiles(version):
            checkSnbt(file)

    write_csv("neu_missing_item_model", files)
    write_ssv("neu_missing_item_model", files)

    bazaarable, nonBazaarable = filterBazaar(files)
    write_csv("bazaarable", bazaarable)
    write_ssv("bazaarable", bazaarable)
    write_csv("nonBazaarable", nonBazaarable)
    write_ssv("nonBazaarable", nonBazaarable)


if __name__ == "__main__":
    Main()
