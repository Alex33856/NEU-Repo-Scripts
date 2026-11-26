from json import JSONDecodeError, load
from pathlib import Path

from alex.utils import getAllItems

usageByKey: dict = {}


def checkItemKeys(path: Path):
    with open(path, "r", encoding="utf-8") as file:
        try:
            data = load(file)
        except JSONDecodeError as ex:
            print(f"Failed to parse {path.name}")
            print(ex)
            return

    for key in data:
        if not usageByKey.get(key):
            usageByKey[key] = 0
        usageByKey[key] += 1


def Main():
    for file in getAllItems():
        checkItemKeys(file)
    print(usageByKey)


if __name__ == "__main__":
    Main()
