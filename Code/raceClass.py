
class Race:

    def __init__(self):
        self.name = self.inputRaceName()
        if self.name is None: raise ValueError("No race name provided.")

        self.dist = self.inputRaceDist()
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
            else: print("\nThis is not a valid distance or points value.\n")

    
    def inputRaceDate(self) -> str:
        """Gets a date (or any string) from the user.
        Returns None if the user enters nothing.
        """
        date = input("Date: ")
        if date != "": return date
        else: return None


    def printRaceDetails(self):
        """Prints the race details with horizontal lines above and below it.
        """
        if self.dist.isnumeric():
            toPrint = f"{self.name}, {self.dist} POINTS, {self.date}"
        else:
            toPrint = f"{self.name} {self.dist}, {self.date}"
        
        print("-" * len(toPrint))
        print(toPrint)
        print("-" * len(toPrint))
