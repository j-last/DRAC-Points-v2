
import json
import os
import time
from Code.FileHandler import FileHandler
from Code.Printer import Printer
from Code.Race import Race

TIME_FORMAT = "%H.%M.%S"
VALID_AGES = ["MU17", "M17-39", "M40-44", "M45-49", "M50-54", "M55-59", "M60-64", "M65+",
                 "WU17", "W17-34", "W35-39", "W40-44", "W45-49", "W50-54", "W55-59", "W60-64", "W65+"]

class Runner:

    def __init__(self, name:str):
        """Converts from file contents -> Runner object
        If the age category is not set, this is resolved here.
        """
        self.fileLines = FileHandler.getFileLines(name)
        self.name = name
        self.ageCat = self.fileLines[1].strip()
        self.points = int(self.fileLines[2][7:].strip())

        if self.ageCat[-1] == "?": self.setAgeCat()
        if self.ageCat in ["MU17", "WU17"]:
            self.parkruns = int(self.fileLines[3][10:].strip())


    @staticmethod
    def exists(name:str) -> bool:
        """Returns True if the runner has a file, otherwise False.
        """
        people = os.listdir("Members")
        if name + ".txt" in people:
            return True
        else: return False


    def printDetails(self) -> None:
        """Prints the race details with horizontal lines above and below it.
        """
        toPrint = f"{self.name}, {self.ageCat}, TOTAL: {self.points}"
        
        Printer.blue("-" * len(toPrint) + "\n" + toPrint + "\n" + "-" * len(toPrint))



    def addToFile(self, race:Race, raceTime:time) -> int:
        """Adds a race to a runner's file.
        """
        points = self.calcPoints(race, raceTime)

        self.points += points

        self.fileLines[2] = "TOTAL: " + str(self.points) + "\n"
            
        if raceTime is not None:
            self.fileLines.append(f"{race.date}, {race.getFullName()}, {time.strftime(TIME_FORMAT, raceTime)}, {points} POINT(S)\n")
        else:
            self.fileLines.append(f"{race.date}, {race.getFullName()}, {points} POINT(S)\n")

        FileHandler.writeFileLines(self.name, self.fileLines)
        Printer.blue(f"ADDED {points} POINTS to {self.name} (TOTAL: {self.points})", "\n")
    

    def calcPoints(self, race:Race, raceTime:time) -> int:
        """Calculates the number of points for a race.
        If the race distance is numeric, then it returns this, so raceTime can be None.
        Otherwise, raceTime cannot be None as this is needed to calculate points.
        """
        if race.dist.isnumeric():
            return int(race.dist)

        standards = open("Code/Standards.json")
        data = json.load(standards)
        standards.close()

        standards = data[self.ageCat][race.dist]

        points = 4
        for standardTime in standards:
            if raceTime <= time.strptime(standardTime, TIME_FORMAT):
                points += 1
        if points == 9: points += 1
        return points
    

    def setAgeCat(self) -> None:
        """Prompts the user to update the persons age category.
        """
        self.printDetails()
        print(f"This person was {self.ageCat}.")

        new_age_cat = None
        while new_age_cat not in VALID_AGES + [""]:
            new_age_cat = input("New age category (type nothing to keep the same): ")
            new_age_cat = new_age_cat.upper()

        if new_age_cat == "":
            self.ageCat = self.ageCat[:-1]
        else:
            self.ageCat = new_age_cat
        self.fileLines[1] = self.ageCat + "\n"
        FileHandler.writeFileLines(self.name, self.fileLines)
