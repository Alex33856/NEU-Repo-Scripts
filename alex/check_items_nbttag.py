from json import JSONDecodeError, load
from pathlib import Path

from nbtlib import InvalidLiteral

from alex.utils import getAllItems
from nbt_utils import parse_nbt

loreIssues = []
displayNameIssues = []
idIssues = []


def checkNbtTag(path: Path):
    with open(path, "r", encoding="utf-8") as file:
        try:
            data = load(file)
        except JSONDecodeError as ex:
            print(f"Failed to parse {path.name}")
            print(ex)
            return

    try:
        text = data["nbttag"]
        tag = parse_nbt(text)
    except InvalidLiteral as ex:
        print(f"Failed to parse {path.name}: nbttag")
        print(ex.args[1])
        print("At: " + text[ex.args[0][0] - 5:ex.args[0][0] + 1] + "<-- [HERE]")
        print(text[ex.args[0][0] + 1: ex.args[0][1] + 5])
        return

    tagName = tag["display"]["Name"]
    if tagName != data["displayname"]:
        displayNameIssues.append(path.name)

    tagId = tag["ExtraAttributes"]["id"]
    if tagId != data["internalname"]:
        idIssues.append(path.name)

    tagLore = tag["display"]["Lore"]
    if len(data["lore"]) != len(tagLore):
        # print(data["lore"])
        # print(tagLore)
        print(f"Lore size difference: {path.name}")
        loreIssues.append(path.name)
        # print("Lore does not match!")
        return

    for i, line in enumerate(data["lore"]):
        tagLine = tagLore[i]
        if line != tagLine:
            # print("A lore line doesn't match!")
            # print(i, line, tag["display"]["Lore"][i])
            print(f"Lore line difference: {path.name}")
            loreIssues.append(path.name)
            return


def printIssue(type: str, issueList: list[str]):
    print(f"Items with {type} issues: {len(issueList)}")
    print(" ".join([x.replace(".json", "") for x in issueList]))


def printAllIssues():
    if displayNameIssues:
        printIssue("display name", displayNameIssues)
    if loreIssues:
        printIssue("lore", loreIssues)
    if idIssues:
        printIssue("id", idIssues)
    if not loreIssues and not displayNameIssues and not idIssues:
        print("No nbttag issues found!")


def Main():
    for file in getAllItems():
        checkNbtTag(file)
    printAllIssues()


if __name__ == "__main__":
    Main()
