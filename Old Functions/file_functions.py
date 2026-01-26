import json
import os
import time
import datetime

timeFormat = "%H.%M.%S"
VALID_AGES = ["MU17", "M17-39", "M40-44", "M45-49", "M50-54", "M55-59", "M60-64", "M65+",
                 "WU17", "W17-34", "W35-39", "W40-44", "W45-49", "W50-54", "W55-59", "W60-64", "W65+"]


def getAgeCat(runnerName):
    """Gets the age category of a runner.
    The runner must exist.
    """

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










