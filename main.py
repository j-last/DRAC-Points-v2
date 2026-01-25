from Code.raceClass import Race

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
    # Get race details
    try: race :Race = Race()
    except ValueError: return


    runnersAdded = 0
    while True:
        race.printRaceDetails()
        print(f"{runnersAdded} RUNNERS ADDED (so far)")
        input()
        # Continually get runner names
        #runnerName = getRunnerName()
        #if runnerName is None: break
        #print(f"\nFILE: {runnerName.upper()}, {getAgeCat(runnerName)}\n")

        # Calculate how many points they should get
       # points = race.calcPoints(ageCat, time)

        # Add it to their file
        #addToFile()
        runnersAdded += 1
        
    print(f"\n{runnersAdded} RUNNERS ADDED")
    #addToHistory(raceName, raceDist)
    
    

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
