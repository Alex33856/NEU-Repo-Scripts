import json

from alex.utils import BasePath, check_for_item

parentsPath = BasePath / "constants" / "parents.json"

with open(parentsPath, "r") as f:
    parents = json.load(f)


def Main():
    allContained = set()

    for key in parents:
        if key in allContained:
            print(f"P: {key} is contained already!")
        allContained.add(key)

        if not check_for_item(key):
            print(f"P: {key} does not exist!")

        currentGroupContained = set()
        for child in parents[key]:
            if child in currentGroupContained:
                print(f"C: {child} already exists in {key}!")

            if child in allContained:
                print(f"C: {child} is already contained elsewhere!")

            if not check_for_item(child):
                print(f"C of {key}: {child} does not exist!")
            currentGroupContained.add(child)
        allContained = allContained.union(currentGroupContained)


if __name__ == "__main__":
    Main()
