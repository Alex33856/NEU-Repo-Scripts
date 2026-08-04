import json

from alex.utils import ConstantsPath, ItemsPath, check_for_item, get_bazaar_products

bazaarStocksPath = ConstantsPath.joinpath("bazaarstocks.json")
with open(bazaarStocksPath) as json_file:
    bazaarStocks = json.load(json_file)

itemNames = ItemsPath
products = get_bazaar_products()

for entry in bazaarStocks:
    if entry['stock'] not in products:
        print(f"Couldn't find stock {entry['stock']} on the Bazaar API!")

    if not check_for_item(entry['id']):
        print(f"Couldn't find item {entry['id']}!")

if __name__ == "__main__":
    pass
