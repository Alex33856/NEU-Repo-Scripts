import json
from os import listdir
from os.path import isfile
from pathlib import Path

from nbtlib import InvalidLiteral

from alex.nbt_utils import parse_nbt
from alex.utils import getSNBTVersions, OverlayPath

unknown_keys = set()
disallowed_keys = ["uuid", "timestamp", "edition"]


def checkItemSnbt(path: Path):
    fileAndDir = str(path.relative_to(path.parent.parent))
    with open(path, "r", encoding="utf-8") as file:
        try:
            text = file.read()
            data = parse_nbt(text)
            del text
        except InvalidLiteral as ex:
            print(f"Failed to parse {path}")
            print(text[ex.args[0][0] - 5: ex.args[0][0] + 1].strip() + "<-- [HERE]")
            print(text[ex.args[0][0] + 1: ex.args[0][1] + 10].strip())
            print(ex.args[1], ex.args[0])
            return

    if not data["components"].get("minecraft:tooltip_display"):
        print(f"warning: {fileAndDir} is missing tooltip display!")

    if not data["components"].get("minecraft:tooltip_style"):
        excludedPaths = ["_MONSTER", "_NPC", "_MINIBOSS", "_BOSS", "_ANIMAL"]
        shouldPrint = True
        for excludedPath in excludedPaths:
            if excludedPath in fileAndDir:
                shouldPrint = False
                break
        if shouldPrint:
            print(f"warning: {fileAndDir} is missing tooltip style!")

    customData = data["components"]["minecraft:custom_data"]
    for key in customData:
        if key not in unknown_keys:
            # print(f"new key: {key}")
            unknown_keys.add(key)

    for key in disallowed_keys:
        if key in customData:
            print(f"warning - {fileAndDir} has disallowed key: {key}")

    if customData.get("petInfo"):
        petInfo = json.loads(customData["petInfo"])
        if petInfo.get("exp", None) is None:
            print(f"warning: {fileAndDir} does not have exp set in pet info!")

    if data["components"].get("minecraft:enchantments"):
        print(f"warning: {fileAndDir} has enchantments set!")


def getSnbtFiles(version):
    path = OverlayPath.joinpath(version)
    dirContents = listdir(path)
    validFiles = []

    for file in dirContents:
        fullPath = path.joinpath(file)
        if isfile(fullPath):
            validFiles.append(fullPath)

    return validFiles


def Main():
    for version in getSNBTVersions():
        for file in getSnbtFiles(version):
            checkItemSnbt(file)


if __name__ == "__main__":
    Main()
