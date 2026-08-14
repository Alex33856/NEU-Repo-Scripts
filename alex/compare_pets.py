import csv
import json
import os
from copy import copy
from dataclasses import dataclass
from typing import Optional

import psycopg
from psycopg import connection, cursor

from alex.utils import get_lore_for_file, ItemsPath, ConstantsPath, rarityMap


@dataclass(slots=True)
class Pet:
    pet_id: str
    pet_level: int
    lore_lines: list[str]


petNumData = {}


def connect() -> tuple[connection.Connection, cursor.Cursor]:
    con = psycopg.connect(**json.loads(os.environ["DB_ARGS"]))
    cur = con.cursor()
    return con, cur


def getPetsDb() -> list[Pet]:
    con, cur = connect()
    cur.execute("SELECT pet_id, pet_level, lore_lines FROM pet_data WHERE pet_level != 102;")
    data = cur.fetchall()

    pets = []
    for row in data:
        pet = Pet(row[0], row[1], row[2])
        pets.append(pet)

    con.close()
    return pets


def getPetsCsv() -> list[Pet]:
    pets = []
    with open("./pet_data.csv", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # ignore header
        for row in reader:
            pet = Pet(row[0], int(row[1]), json.loads(row[2]))
            pets.append(pet)
    return pets


def getPets() -> list[Pet]:
    if os.environ.get("DB_ARGS"):
        return getPetsDb()
    else:
        return getPetsCsv()


def loadPetNums():
    global petNumData
    with open(ConstantsPath / "petnums.json") as file:
        petNumData = json.load(file)


def getAppliedLore(pet: Pet) -> Optional[list[str]]:
    templateLore = get_lore_for_file(ItemsPath / f"{pet.pet_id}.json")
    if templateLore is None:
        print(f"Unknown pet: {pet.pet_id}")
        return None

    (petId, rarityIndex) = pet.pet_id.split(";")
    rarity = rarityMap[int(rarityIndex)]
    thisPetsData = petNumData[petId][rarity]
    petLevel = pet.pet_level
    if petLevel > 100:
        petLevel -= 100
    thisLevelsData = thisPetsData[str(petLevel)]

    appliedLore = []
    for line in templateLore:
        newLine = line
        otherNums = thisLevelsData["otherNums"]
        statNums = thisLevelsData["statNums"]
        for i, otherNum in enumerate(otherNums):
            replacement = str(otherNums[i])
            newLine = newLine.replace("{" + str(i) + "}", replacement)
        for stat in thisLevelsData["statNums"]:
            replacement = str(statNums[stat])
            newLine = newLine.replace("{" + stat + "}", replacement)
        appliedLore.append(newLine)

    return appliedLore


def comparePet(pet: Pet) -> bool:
    knownLore = pet.lore_lines
    appliedLore = getAppliedLore(pet)
    if appliedLore is None:
        return False

    if knownLore == appliedLore:
        return True

    newLore = copy(appliedLore)
    for i, line in enumerate(appliedLore):
        newLore[i] = line.replace(".0", "")

    if knownLore == newLore:
        return True

    print(f"Mismatch for {pet.pet_id} lvl {pet.pet_level}")

    if (kLL := len(knownLore)) != (aLL := len(appliedLore)):
        print(f"Size diff: {kLL} vs {aLL}")

    for i, line in enumerate(knownLore):
        if len(appliedLore) <= i:
            break
        genLine = appliedLore[i]
        genLineClean = newLore[i]
        if line == genLine or line == genLineClean:
            continue

        print(f"Differing Line:\n- {line}\n+ {genLine}")

    return False


def Main():
    loadPetNums()
    pets = getPets()
    mismatching = set()
    for pet in pets:
        if pet.pet_id in mismatching:
            continue
        if not comparePet(pet):
            mismatching.add(pet.pet_id)


if __name__ == "__main__":
    Main()
