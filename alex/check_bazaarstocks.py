import json

import requests

from alex.utils import ConstantsPath, ItemsPath, check_for_item

bazaarStocksPath = ConstantsPath.joinpath("bazaarstocks.json")
with open(bazaarStocksPath) as json_file:
    bazaarStocks = json.load(json_file)

itemNames = ItemsPath

bazaarData = requests.get("https://api.hypixel.net/v2/skyblock/bazaar").json()
products = bazaarData["products"].keys()

for entry in bazaarStocks:
    if entry['stock'] not in products:
        print(f"Couldn't find stock {entry['stock']} on the Bazaar API!")

    if not check_for_item(entry['id']):
        print(f"Couldn't find item {entry['id']}!")

if __name__ == "__main__":
    pass
