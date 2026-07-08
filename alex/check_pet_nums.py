import json
import re
from copy import copy
from typing import Optional

from alex.utils import BasePath, rarityMap, get_lore_for_file

petNumsPath = BasePath.joinpath("constants").joinpath("petnums.json")
with open(petNumsPath, "r") as f:
    petNums = json.load(f)

lorePetNumRe = re.compile("{([0-9A-Z_]+)}")


def get_lore_for_pet(petId) -> Optional[list[str]]:
    path = BasePath.joinpath("items").joinpath(petId + ".json")
    return get_lore_for_file(path)


def check_pet(pet, rarity):
    itemId = f"{pet};{rarityMap.index(rarity)}"
    petData = petNums[pet][rarity]
    keys = list(petData.keys())
    if "stats_levelling_curve" in keys:
        keys.remove("stats_levelling_curve")

    otherNumsSize = None
    statNumKeys = None

    for key in keys:
        thisOtherNumsSize = len(petData[key]["otherNums"])
        thisStatNumsSize = petData[key]["statNums"].keys()
        if otherNumsSize is None:
            otherNumsSize = thisOtherNumsSize
        if statNumKeys is None:
            statNumKeys = thisStatNumsSize
        assert otherNumsSize == thisOtherNumsSize, f"Other Nums differ in length for {itemId}"
        assert statNumKeys == thisStatNumsSize, f"Stat Nums are different for {itemId}"

    if statNumKeys is None:
        statNumKeys = []

    if otherNumsSize is None:
        otherNumsSize = 0

    allKeys = list(statNumKeys) + list(str(x) for x in range(0, otherNumsSize))
    unusedKeys = copy(allKeys)
    lore = get_lore_for_pet(itemId)
    assert lore is not None, f"Pet nums found for {itemId} without an item existing"
    for line in lore:
        matches = lorePetNumRe.findall(line)
        for match in matches:
            if match in unusedKeys:
                unusedKeys.remove(match)
            else:
                if match not in allKeys:
                    raise AssertionError(f"Found unknown key for {itemId}: {match}")
    assert len(unusedKeys) == 0, f"Not all pet nums are used for {itemId}: {unusedKeys}"


def check_pets():
    for pet in petNums:
        for rarity in petNums[pet]:
            try:
                check_pet(pet, rarity)
            except AssertionError as ex:
                print(ex)


if __name__ == "__main__":
    check_pets()
