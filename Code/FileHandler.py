

import datetime
import os

from Code.Printer import Printer
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


    @staticmethod
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
        File in the form 'FIRSTNAME LASTNAME.txt' will be created containing the default file lines.
        """
        while True:
            name = input("Create file for name: ").strip().upper()
            if name == "":
                Printer.red("\nNo new file created.")
                return
            if name + ".txt" in os.listdir("Members"):
                Printer.red("A file already exists for that name. No new file created.")
                return
            elif len(name.split()) == 2: 
                break
            Printer.red("\nPlease write in the form <firstname> <lastname>.")

        while True:
            ageCat = input(f"Age category for {name}: ").upper()
            if ageCat == "": 
                Printer.red("\nNo new file created.")
                return
            elif ageCat in VALID_AGES: 
                break
            Printer.red("\nNot a valid age category.")
        if ageCat in ["MU17", "WU17"]:
            fileLines = [name, "\n", ageCat, "\n", "TOTAL: 0\n", "PARKRUNS: 0\n" "------------------------------\n"]
        else:
            fileLines = [name, "\n", ageCat, "\n", "TOTAL: 0\n", "------------------------------\n"]
        FileHandler.writeFileLines(name, fileLines)
        print(f"\nFILE CREATED FOR '{name}'.\n")
        return name
    

    @staticmethod
    def getParkrunDict():
        """Opens parkruns.txt and converts the data to a dictionary format {name : total}
        """
        parkrun_file = open("Parkruns/parkruns.txt", "r")
        lines = parkrun_file.readlines()
        parkrun_file.close()

        newlines = {}
        for line in lines:
            name, total = line.split(" - ")
            total = int(total)
            newlines[name] = total
        return newlines
    

    @staticmethod
    def writeParkruns(parkrun_dict):
        """Writes a parkrun dictionary in the form {name : total} to parkruns.txt
        """
        sorted_parkruns = []
        for name, number in parkrun_dict.items():
            sorted_parkruns.append((number, name))
        sorted_parkruns.sort(reverse=True)

        parkrun_file = open("Parkruns/parkruns.txt", "w")
        for number, name in sorted_parkruns:
            parkrun_file.write(f"{name} - {number}\n")
        parkrun_file.close()
    

    @staticmethod
    def addToHistory(race:Race):
        """Adds a race to the history.txt file
        """
        f = open("history.txt", "r")
        filelines = f.readlines()
        f.close()

        todaysDate = datetime.date.strftime(datetime.date.today(), "%d/%m/%y")
        filelines.insert(0, f"{todaysDate}, {race.getFullName()}\n")

        f = open("history.txt", "w")
        f.writelines(filelines)
        f.close()