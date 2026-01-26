

import datetime
import os

from Code.Race import Race

VALID_AGES = ["MU17", "M17-39", "M40-44", "M45-49", "M50-54", "M55-59", "M60-64", "M65+",
                 "WU17", "W17-34", "W35-39", "W40-44", "W45-49", "W50-54", "W55-59", "W60-64", "W65+"]

class FileHandler:

    @staticmethod
    def getFileLines(name:str):
        """Gets the file lines of a runner's file in a list format.
        The runner must exist.
        """

        personFile = open(os.path.join("Members", name + ".txt"), "r")
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

    @staticmethod
    def createFile():
        """Prompts the user to create a new runner file.
        File in the form FIRSTNAME LASTNAME.txt will be created.
        """
        while True:
            name = input("Create file for name: ").strip()
            if name == "":
                print("\nNo new file created.")
                return
            elif len(name.split()) == 2: 
                break
            print("\nPlease write in the form <firstname> <lastname>.")
        
        name = name.upper()

        while True:
            ageCat = input(f"Age category for {name}: ").upper()
            if ageCat == "": 
                print("\nNo new file created.")
                return
            elif ageCat in VALID_AGES: 
                break
            print("\nNot a valid age category.")
        
        fileLines = [name, "\n", ageCat, "\n", "TOTAL: 0\n", "------------------------------\n"]
        FileHandler.writeFileLines(name, fileLines)
        print(f"\nFILE CREATED FOR '{name}'.\n")
        return name
    

    def addToHistory(race:Race):
        """Adds a race to the history.txt file
        """
        f = open("history.txt", "r")
        filelines = f.readlines()
        f.close()

        todaysDate = datetime.date.strftime(datetime.date.today(), "%d/%m/%y")
        filelines.insert(0, f"{todaysDate}, {race.getFullName}\n")

        f = open("history.txt", "w")
        f.writelines(filelines)
        f.close()