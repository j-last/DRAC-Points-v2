import json
import os
import time
import datetime
from Code.string_functions import *

timeFormat = "%H.%M.%S"
VALID_AGES = ["MU17", "M17-39", "M40-44", "M45-49", "M50-54", "M55-59", "M60-64", "M65+",
                 "WU17", "W17-34", "W35-39", "W40-44", "W45-49", "W50-54", "W55-59", "W60-64", "W65+"]


def resolvePartName(partName:str):
    """Attempts to match a partial name to a file.
    Returns the name if it was successful, otherwise None.
    """
    if len(partName.split()) < 2:
        return None # Name does not have a space in it
    name = ""
    partFirst, partLast = partName.split()[0], partName.split()[-1]
    for fileName in os.listdir("Members"):
        firstName, lastName = fileName[:-4].split()
        if firstName[:len(partFirst)] == partFirst and lastName[:len(partLast)] == partLast:
            if name != "": return None # Part name refers to multiple people
            name = fileName[:-4]
    if name == "": return None
    return name


def getAgeCat(runnerName):
    """Gets the age category of a runner.
    The runner must exist.
    """
    assert runnerExists(runnerName)

    f = open(os.path.join("Members", runnerName + ".txt"), "r")
    lines = f.readlines()
    ageCat = lines[1][:-1] # removes newline character
    f.close()

    # changing age categories if not already done so
    if ageCat[-1] == "?":
        ageCat = ageCat[:-1]
        print(runnerName.upper())

        if ageCat == "MU40": ageCat = "M17-39"
        elif ageCat == "WU35": ageCat = "W17-34"

        print(f"This person was {ageCat}.")

        new_age_cat = None
        while new_age_cat not in VALID_AGES + [""]:
            new_age_cat = input("New age category (type nothing to keep the same): ")
            new_age_cat = new_age_cat.upper()

        if new_age_cat == "":
            new_age_cat = ageCat

        lines[1] = ageCat + "\n"

        f = open(os.path.join("Members", runnerName + ".txt"), "w")
        f.writelines(lines)
        f.close()
        ageCat = new_age_cat
    
    return ageCat










