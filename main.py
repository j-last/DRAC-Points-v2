import time
from colorama import Fore
from Code.FileHandler import FileHandler
from Code.Runner import Runner
from Code.WebScraper import WebScraper
from Code.NameResolver import NameResolver
from Code.Race import Race

# constants
TIME_FORMAT = "%H.%M.%S"

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


def manualRaceEntry():
    try: race :Race = Race()
    except ValueError: return

    runnersAdded = 0
    while True:
        race.printDetails(runnersAdded)

        runner = NameResolver.getRunnerFromUser()
        if runner is None: break
        runner.printDetails()
        runner.addToFile(race, race.getTime())

        runnersAdded += 1
        
    print(f"\n{runnersAdded} RUNNERS ADDED")
    FileHandler.addToHistory(race)


def urlRaceEntry():
    try: race :Race = Race()
    except ValueError: return
    runnersAdded = 0
    race.printDetails(runnersAdded)

    try:
        url = input("Copy and paste the totalRaceTiming URL: ")
        if url == "": return
        runnersAndTimes = WebScraper.getTotalRaceTimingResults(url)
    except:
        print(Fore.RED + "Something went wrong." + Fore.RESET + "\n")
        return

    toAdd, notAdded = [], []
    for runnerName, raceTime in runnersAndTimes.items():
        if Runner.exists(runnerName):
            toAdd.append((Runner(runnerName), raceTime))
        else:
            # MOVE THIS CODE INTO NAME RESOLVE METHOD
            print(Fore.RED)
            response = input(f"{runnerName} could not be found. Type 'c' to create a file or leave blank to get the option to type their name in: ")
            if response == "c":
                runner = FileHandler.createFile()
                if runner is None:
                    print(Fore.RED + f"No result will be added for {runnerName}." + Fore.RESET + "\n")
                    notAdded.append((runnerName, raceTime))
                else:
                    toAdd.append((Runner(runnerName), raceTime))
            else:
                runner = NameResolver.getRunnerFromUser()
                if runner is None:
                    print(Fore.RED + f"No result will be added for {runnerName}.")
                    print(Fore.RESET)
                    notAdded.append((runnerName, raceTime))
                else:
                    toAdd.append((runner, raceTime))
            # ------------------------------------------
    
    print(Fore.BLUE)
    for runner, raceTime in toAdd:
        print(f"{runner.name} - {time.strftime(TIME_FORMAT, raceTime)}")
    print(Fore.RESET)
    answer = input("ADD THESE RESULTS? (y/n) ")
    if answer.lower() == "y":
        print(Fore.BLUE)
        for runner, raceTime in toAdd:
            runner.addToFile(race, raceTime)
            runnersAdded += 1
        print(Fore.RESET)
    
    print(f"{runnersAdded} RUNNERS ADDED")

    if len(notAdded) > 0:
        print(Fore.RED)
        print("NOT ADDED: ")
        for runnerName, raceTime in notAdded:
            print(f"{runnerName}, {time.strftime(TIME_FORMAT, raceTime)}")
        print(Fore.RESET)

    FileHandler.addToHistory(race)
    

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
