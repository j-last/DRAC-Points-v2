import os


def runnerExists(runnerName:str) -> bool:
    people = os.listdir("Members")
    if runnerName + ".txt" in people:
        return True
    else: return False


def resolvePartName(partName:str):
    if len(partName.split()) != 2:
        print("This name can't be used with part names.")
        return
    name = ""
    partFirst, partLast = partName.split()
    for fileName in os.listdir("Members"):
        firstName, lastName = fileName[:-4].split()
        if firstName[:len(partFirst)] == partFirst and lastName[:len(partLast)] == partLast:
            if name != "":
                print("This partial name refers to multiple people, please try again")
                return ""
            name = fileName[:-4]
    return name


def getFileLines(runnerName:str):
    personFile = open(os.path.join("Members", runnerName + ".txt"), "r")
    fileLines = personFile.readlines()
    personFile.close()
    return fileLines


def writeFileLines(name, lines_to_write):
    personFile = open(os.path.join("Members", name + ".txt"), "w")
    personFile.writelines(lines_to_write)
    personFile.close()


def addToFile(runnerName:str, pointsToAdd:int, *args) -> bool:
    fileLines = getFileLines(runnerName)

    newPoints = int(fileLines[2].strip()[6:]) + pointsToAdd
    fileLines[2] = "TOTAL: " + str(newPoints) + "\n"

    lineToAdd = ""
    for arg in args:
        lineToAdd += f"{arg}, "
    lineToAdd += f"{pointsToAdd} POINTS\n"

    fileLines.append(lineToAdd)
    writeFileLines(fileLines)
    print(f"{pointsToAdd} POINTS added to {runnerName.upper()} (Total: {newPoints})")
