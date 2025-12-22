from Code.file_functions import *

def getRaceName() -> str:
    return input("Race Name: ")


def getRaceDist() -> str:
    validDistances = ["5k", "5mi", "10k", "10mi", "half","20mi", "mara"]
    while True:
        raceDist = input("Distance (or points num): ")
        if raceDist == "": return ""
        elif raceDist in validDistances: return raceDist # race dist is a valid distance
        elif raceDist.isnumeric(): return raceDist # race dist is a valid points value
        else: print("This is not a valid distance or points value.")


def getRaceDate() -> str:
    return input("Date: ")


def getRunnerName() -> str:
    runnerName = " "
    while runnerName != "":
        runnerName = capitaliseName(input("Runner Name: "))
        if runnerExists(runnerName):
            return runnerName
        else:
            runnerName = resolvePartName(runnerName)
            if runnerName == "": runnerName = " "
            else: return runnerName
    

def capitaliseName(runnerName:str) -> str:
    runnerName = runnerName.strip().lower()
    runnerName = list(runnerName)
    
    runnerName[0] = runnerName[0].upper()
    for i in range(len(runnerName)):
        if runnerName[i] in [" ", "-"]:
            runnerName[i+1] = runnerName[i+1].upper()
    
    capitalisedName = ""
    for char in runnerName: capitalisedName += char
    return capitalisedName
