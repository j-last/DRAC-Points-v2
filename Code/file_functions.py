import json
import os
import time
import datetime
from Code.string_functions import *

timeFormat = "%H.%M.%S"
VALID_AGES = ["MU17", "M17-39", "M40-44", "M45-49", "M50-54", "M55-59", "M60-64", "M65+",
                 "WU17", "W17-34", "W35-39", "W40-44", "W45-49", "W50-54", "W55-59", "W60-64", "W65+"]

# Getting names of runners
def runnerExists(runnerName:str) -> bool:
    """Returns True if the runner name exists, otherwise False.
    """
    people = os.listdir("Members")
    if runnerName + ".txt" in people:
        return True
    else: return False


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


def createFile():
    """Prompts the user to create a new runner file.
    File in the form Firstname Lastname.txt will be created.
    """
    runnerName = input("Create file for name: ").strip()
    while len(runnerName.split()) != 2:
        print("\nPlease write in the form <firstname> <lastname>.")
        runnerName = input("Name: ").strip()
    
    runnerName = capitaliseName()

    ageCat = ""
    while ageCat not in VALID_AGES:
        ageCat = input(f"Age category for {runnerName}: ").upper()
    
    fileLines = [runnerName, "\n", ageCat, "\n", "POINTS: 0\n", "PARKRUNS: 0\n\n"]
    writeFileLines(runnerName, fileLines)
    print(f"\nFILE CREATED FOR {runnerName}.\n")
    return runnerName


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


def calcPoints(runnerName:str, raceTime:time, raceDist:str):
    """Calculates the number of points to give a runner using the race distance and the time they got.
    The runner must exist.
    """
    assert runnerExists(runnerName)

    standards = open("Code/Standards.json")
    data = json.load(standards)
    standards.close()

    ageCat = getAgeCat(runnerName)

    standards = data[ageCat][raceDist]

    points = 4
    for standardTime in standards:
        if raceTime <= time.strptime(standardTime, timeFormat):
            points += 1
    if points == 9: points += 1
    return points


def getFileLines(runnerName:str):
    """Gets the file lines of a runner's file in a list format.
    The runner must exist.
    """
    assert runnerExists(runnerName)

    personFile = open(os.path.join("Members", runnerName + ".txt"), "r")
    fileLines = personFile.readlines()
    personFile.close()
    return fileLines


def writeFileLines(name, lines_to_write):
    """Writes a list of file lines to a runner's file.
    The runner doesn't have to exist.
    """
    personFile = open(os.path.join("Members", name + ".txt"), "w")
    personFile.writelines(lines_to_write)
    personFile.close()


def addToFile(runnerName:str, pointsToAdd:int, *args) -> bool:
    """Adds a race to a runner's file.
    """
    fileLines = getFileLines(runnerName)

    newPoints = int(fileLines[2].strip()[8:]) + pointsToAdd
    fileLines[2] = "POINTS: " + str(newPoints) + "\n"

    lineToAdd = ""
    for arg in args:
        lineToAdd += f"{arg}, "
    lineToAdd += f"{pointsToAdd} POINTS\n"

    fileLines.append(lineToAdd)
    writeFileLines(runnerName, fileLines)
    print(f"\n{pointsToAdd} POINTS added to {runnerName.upper()} (POINTS: {newPoints})\n")


def addToHistory(raceName, raceDist):
    """Adds a race to the history.txt file
    """
    f = open("history.txt", "r")
    filelines = f.readlines()
    f.close()

    todaysDate = datetime.date.strftime(datetime.date.today(), "%d/%m/%y")
    filelines.insert(0, f"{todaysDate}, {raceName} {raceDist}\n")

    f = open("history.txt", "w")
    f.writelines(filelines)
    f.close()
