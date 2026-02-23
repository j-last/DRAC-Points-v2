
import time

from Code.Printer import Printer

TIME_FORMAT = "%H.%M.%S"
VALID_AGES = ["MU17", "M17-39", "M40-44", "M45-49", "M50-54", "M55-59", "M60-64", "M65+",
                 "WU17", "W17-34", "W35-39", "W40-44", "W45-49", "W50-54", "W55-59", "W60-64", "W65+"]

class Race:

    def __init__(self, name=None, dist=None):
        """Instantiates a Race object by asking the user for it's name, distance and date (if not provided in the args)
        Raises a ValueError if the user enters nothing for any of these.
        """
        if name is not None: self.name = name
        else: self.name = self.inputRaceName()
        if self.name is None: raise ValueError("No race name provided.")

        if dist is not None: self.dist = dist
        else: self.dist = self.inputRaceDist()
        if self.dist is None: raise ValueError("No race distance provided.")

        self.date = self.inputRaceDate()
        if self.date is None: raise ValueError("No race date provided.")

    
    def inputRaceName(self) -> str:
        """Gets the name of a race from the user.
        Returns None if the user enters nothing.
        """
        raceName = input("Race Name: ")
        if raceName != "": return raceName
        else: return None


    def inputRaceDist(self) -> str:
        """Continually asks the user for a distance or points value until a valid one is entered.
        Returns None if the user enters nothing.
        """
        validDistances = ["5k", "5mi", "10k", "10mi", "half","20mi", "mara"]
        while True:
            dist = input("Distance (or points num): ")
            if dist == "": return None
            elif dist in validDistances: return dist # race dist is a valid distance
            elif dist.isnumeric(): return dist # race dist is a valid points value
            else: Printer.yellow("\nThis is not a valid distance or points value.\n")

    
    def inputRaceDate(self) -> str:
        """Gets a date (or any string) from the user.
        Returns None if the user enters nothing.
        """
        date = input("Date: ")
        if date != "": return date
        else: return None


    def getFullName(self) -> str:
        """Returns the name and distance of the race as a string.
        E.g. name='Wroxham', dist='5k' returns 'Wroxham 5k'"""
        if self.dist.isnumeric():
            return self.name
        return self.name + " " + self.dist


    def printDetails(self, runnersAdded:int) -> None:
        """Prints the race details with horizontal lines above and below it.
        """
        if self.dist.isnumeric():
            toPrint = f"{self.name}, {self.dist} POINTS, {self.date} - {runnersAdded} runners added so far."
        else:
            toPrint = f"{self.name} {self.dist}, {self.date} - {runnersAdded} runners added so far."
        Printer.green("-" * len(toPrint) + "\n" + toPrint + "\n" + "-" * len(toPrint))


    def getTime(self) -> time:
        """Gets the user to enter a time for a race.
        Instantly returns None if the race distance is numeric (as this doesn't require a time)
        Returns an empty string if the user enters nothing.
        """
        if self.dist.isnumeric():
            return
        while True:
            raceTime = input("Time: ")
            if raceTime == "": return ""
            elif raceTime.count(".") == 1:
                raceTime = "0." + raceTime

            try:
                raceTime = time.strptime(raceTime, TIME_FORMAT)
                return raceTime
            except ValueError:
                Printer.red(f"Invalid time format '{raceTime}'. Please try again.")


 