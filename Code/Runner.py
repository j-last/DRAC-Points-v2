
import json
import os
import time
from colorama import Fore

from Code.FileHandler import FileHandler
from Code.Race import Race
TIME_FORMAT = "%H.%M.%S"

class Runner:

    def __init__(self, name:str):
        if Runner.exists(name):
            self.fileLines = FileHandler.getFileLines(name)
            self.name = name
            self.ageCat = self.fileLines[1].strip()
            self.points = int(self.fileLines[2][7:].strip())


    @staticmethod
    def exists(name):
        """Returns True if the runner name exists, otherwise False.
        """
        people = os.listdir("Members")
        if name + ".txt" in people:
            return True
        else: return False


    def printDetails(self):
        """Prints the race details with horizontal lines above and below it.
        """
        toPrint = f"{self.name}, {self.ageCat}, TOTAL: {self.points}"
        
        print(Fore.BLUE)
        print("-" * len(toPrint))
        print(toPrint)
        print("-" * len(toPrint))
        print(Fore.RESET)


    def addToFile(self, race:Race, raceTime:time) -> int:
        """Adds a race to a runner's file.
        """
        points = self.calcPoints(race, raceTime)

        self.points += points

        self.fileLines[2] = "TOTAL: " + str(self.points) + "\n"
        
        if raceTime is not None:
            self.fileLines.append(f"{race.getFullName()}, {time.strftime(TIME_FORMAT, raceTime)}, {race.date}, {points} POINTS\n")
        else:
            self.fileLines.append(f"{race.getFullName()}, {points} POINTS\n")

        FileHandler.writeFileLines(self.name, self.fileLines)
        print(f"ADDED {points} POINTS to {self.name} (TOTAL: {self.points})")
    

    def calcPoints(self, race, raceTime):
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
