"""



DRAC CLUB POINTS

CLICK PLAY BUTTON (TOP RIGHT) TO START




























"""

import os
import time
import datetime
import shutil
from Code.functions import *
from Code.file_functions import *
from Code.input_functions import *
from Code.scrape_functions import *

# constants
timeFormat = "%H.%M.%S"

# main code
def mainloop():
    while True:
        print("""------------------------------------------------------
T: TotalRaceTiming Link
P: Parkrun Website
              
R: Manual race results
              
E: Backup & Exit
------------------------------------------------------""")
        action = input().upper()
        if action == "R": manualRaceEntry()
        elif action == "T": urlRaceEntry()
        elif action == "P": addParkrunsAuto()
        elif action == "E": backup(); break
        else: print("Not a valid option. Please try again.")


def urlRaceEntry():
    raceName = getRaceName()
    raceDist = getRaceDist()
    raceDate = getRaceDate()

    # gets runners and times

    # checks all runners exist and creates a list of (runners, times & points) to be added
    # user confirms and these are all added

    # anyone not added is looped through asking for an alternative name

    # add to history
    pass
    


def manualRaceEntry():
    raceName = getRaceName()
    raceDist = getRaceDist()
    raceDate = getRaceDate()

    runnersAdded = 0
    while True:
        runnerName = getRunnerName()
        if runnerName == "": 
            return

    # continually loops, asking for a name, checking it exists
    # then asks for a time and adds points to file
    pass
    
    


def addParkrunsAuto():
    # get date

    # gets list of all runners and adds 1 to their total in parkruns.txt
    # ignores names in the dont add to parkrun file

    # tries to add 1 point for juniors, up to 10 parkruns
    # asks if any other juniors ran in the not added list
    pass

    


def backup():
    # updates the summary sheet
    # copies all members across to a backup folder with todays date
    # copies summary sheet + parkrun sheet across to this file
    pass


mainloop()

