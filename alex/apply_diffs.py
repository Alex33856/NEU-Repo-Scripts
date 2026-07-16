import csv
import json
from dataclasses import dataclass
from typing import List

from alex.utils import ItemsPath


@dataclass(slots=True)
class Diff:
    itemId: str
    originalLine: str
    newLine: str


def get_diffs() -> List[Diff]:
    diff_path = input("Absolute path to diffs: ")
    if diff_path.startswith("\"") and diff_path.endswith("\""):
        diff_path = diff_path[1:-1]

    with open(diff_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)

        itemId, originalLine, newLine = (-1, -1, -1)
        try:
            itemId = headers.index("item_id")
            originalLine = headers.index("original_line")
            newLine = headers.index("new_line")
        except ValueError:
            print("Invalid format for diffs!")

        diffs = []
        for parts in reader:
            diffs.append(Diff(parts[itemId], parts[originalLine], parts[newLine]))

    return diffs


def apply_diff(itemId: str, diffs: list[Diff]):
    file = ItemsPath.joinpath(itemId + ".json")
    if not file.exists():
        print(f"{file} does not exist!")
        return

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    lore = data['lore']

    appliedDiff = False
    for diff in diffs:
        try:
            index = lore.index(diff.originalLine)
            lore[index] = diff.newLine
            appliedDiff = True
        except ValueError:
            print(f"Failed to find line {diff.originalLine} in {itemId}")

    if not appliedDiff:
        return

    with open(file, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def group_diffs(diffs: list[Diff]) -> dict[str, list[Diff]]:
    diffMap = {}
    for diff in diffs:
        if diff.itemId not in diffMap:
            diffMap[diff.itemId] = []
        diffMap[diff.itemId].append(diff)

    return diffMap


def Main():
    diffs = get_diffs()
    diffMap = group_diffs(diffs)
    for item in diffMap:
        apply_diff(item, diffMap[item])


if __name__ == "__main__":
    Main()
