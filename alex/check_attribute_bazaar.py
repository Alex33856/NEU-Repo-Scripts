import json

from alex.utils import get_bazaar_products, ConstantsPath

products = get_bazaar_products()

with open(ConstantsPath / "attribute_shards.json") as file:
    data = json.load(file)

bazaarMap = {}
with open(ConstantsPath / "bazaarstocks.json") as file:
    bazaar_stocks = json.load(file)
    for entry in bazaar_stocks:
        bazaarMap[entry["id"]] = entry["stock"]

missing_bz_stocks = []
for attribute in data["attributes"]:
    bazaarId = attribute["bazaarName"]
    internalName = attribute["internalName"]
    if bazaarId not in products:
        print(f"Attribute ({bazaarId} / {internalName}) not found in Bazaar Products!")

    if internalName in bazaarMap:
        if bazaarMap[internalName] != bazaarId:
            print(f"mismatching id for {internalName} ({bazaarMap[internalName]} to {bazaarId})")
    else:
        missing_bz_stocks.append({"id": internalName, "stock": bazaarId})
print(json.dumps(missing_bz_stocks, indent=2))

if __name__ == "__main__":
    pass
