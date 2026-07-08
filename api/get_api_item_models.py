import json

with open("items.json", "r", encoding="utf-8") as file:
    data = json.load(file)

itemModels = {}
for item in data["items"]:
    itemId = item["id"]
    itemModel = item.get("item_model")
    if not itemModel:
        continue
    itemModels[itemId] = itemModel

def write_csv():
    with open("api_item_models.csv", "w", encoding="utf-8") as file:
        file.write("item_id,item_model\n")
        for entry in itemModels:
            file.write(entry)
            file.write(",")
            file.write(itemModels[entry])
            file.write("\n")

if __name__ == "__main__":
    write_csv()
