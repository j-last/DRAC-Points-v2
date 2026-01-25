import time
from Code.string_functions import *
from Code.file_functions import *

TIME_FORMAT = "%H.%M.%S"










def getRunnerName() -> str:
    """Continually asks the user for a runner's name until it can be resolved to someone who exists or a new file is created.
    Returns None if the user enters nothing.
    """
    while True:
        runnerName = input("Runner Name: ")
        if runnerName == "": return None
        runnerName = capitaliseName(runnerName)
        
        if runnerExists(runnerName): 
            return runnerName
        else:
            runnerName = resolvePartName(runnerName)
            if runnerName is not None: return runnerName
        create = input("This could not be resolved to a member. Create a file (y/n): ").lower()
        if create == "y":
            runnerName = createFile()
            return runnerName
    


def getRaceTime():
    while True:
        raceTime = input("Time: ")
        if raceTime == "": return
        elif raceTime.count(".") == 1:
            raceTime = "0." + raceTime

        try:
            raceTime = time.strptime(raceTime, TIME_FORMAT)
            return raceTime
        except ValueError:
            print(f"Invalid time format '{raceTime}'. Please try again.")
