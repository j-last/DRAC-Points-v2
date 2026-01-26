import datetime
import os
import shutil
import time
from colorama import Fore
from Code.FileHandler import FileHandler
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
L: List of names
              
E: Backup & Exit
------------------------------------------------------""")
        action = input().upper()
        
        if action == "T": urlRaceEntry()
        elif action == "P": addParkrunsAuto()
        elif action == "R": manualRaceEntry()
        elif action == "L": listOfNames()
        elif action == "E": backup(); break
        else: print("Not a valid option. Please try again.")


def urlRaceEntry():
    # Race details
    try: race :Race = Race()
    except ValueError: return
    runnersAdded = 0
    race.printDetails(runnersAdded)

    # get url and scrape runners & times, outputting an error if anything is not right (like times in weird formats)
    try:
        url = input("Copy and paste the totalRaceTiming URL: ")
        if url == "": return
        runnersAndTimes = WebScraper.getTotalRaceTimingResults(url)
    except:
        print(Fore.RED + "Something went wrong." + Fore.RESET + "\n")
        return

    # Resolve all names, creating a list of (name that exists, their time)
    # Anyone not resolved added to a seperate list
    toAdd, notAdded = [], []
    for runnerName, raceTime in runnersAndTimes.items():
        runner = NameResolver.getRunnerFromName(runnerName)
        if runner is not None:
            toAdd.append((runner, raceTime))
        else:
            print(Fore.RED + f"No result will be added for {runnerName}." + Fore.RESET + "\n")
            notAdded.append((runnerName, raceTime))
    
    # Display all results that will be added before they're added
    print(Fore.BLUE)
    for runner, raceTime in toAdd:
        print(f"{runner.name} - {time.strftime(TIME_FORMAT, raceTime)}")
    print(Fore.RESET)
    answer = input("ADD THESE RESULTS? (y/n) ")
    if answer.lower() == "y":
        # add the results
        print(Fore.BLUE)
        for runner, raceTime in toAdd:
            runner.addToFile(race, raceTime)
            runnersAdded += 1
        print(Fore.RESET)
    else:
        print(Fore.RED + "No results added" + Fore.RESET)
        return
    
    print(f"{runnersAdded} RUNNERS ADDED")

    # Display all not added results before exiting to main menu
    if len(notAdded) > 0:
        print(Fore.RED)
        print("NOT ADDED: ")
        for runnerName, raceTime in notAdded:
            print(f"{runnerName} - {time.strftime(TIME_FORMAT, raceTime)}")
        print(Fore.RESET)

    FileHandler.addToHistory(race)
    

def addParkrunsAuto():
    try: race :Race = Race("parkrun", 1)
    except ValueError: return

    with open("Parkruns/don't add to parkrun list.txt") as f:
        dontAdd = f.readlines()
        dontAdd = list(map(str.upper, map(str.strip, dontAdd)))

    web_text = input("CTRL+A then CTRL+C on the consolodated report website and CTRL+V here: ")
    runners = WebScraper.getParkrunners(web_text)

    newlines = FileHandler.getParkrunDict()
    runners_added = 0
    not_added = []
    for name in runners:
        if name in dontAdd: 
            print(Fore.RED + f"{name} is being ignored" + Fore.RESET)
            continue

        if newlines.get(name) is not None:
            newlines[name] += 1
        else:
            newlines[name] = 1
        runners_added += 1
        print(f"{name.upper()} has now done {newlines[name]} parkruns.")

        runner = NameResolver.getRunnerFromName(name)
        if runner is not None:
            if runner.ageCat in ["MU17", "WU17"]:
                if runner.parkruns < 10:
                    runner.addToFile(race, None)
                    continue
                print(f"{runner.name} has done more than 10 parkruns, no points added.")
            print(f"{runner.name} is not a junior, no points added.")
                

    FileHandler.writeParkruns(newlines)

    print(f"{runners_added} runners have been added.")

    FileHandler.addToHistory(race)


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


def listOfNames():
    try: race :Race = Race()
    except ValueError: return
    if not race.dist.isnumeric():
        print(Fore.RED + "A list of names can only be done for a race with a fixed amount of points." + Fore.RESET)
        return
    
    stringList = input("Enter a list of names, separated by commas (,):\n").upper()

    try:
        nameList = stringList.split(",")
    except:
        print(Fore.RED + "List is in an invalid format." + Fore.RESET)
        return
    
    for i in range(len(nameList)):
        nameList[i] = NameResolver.resolveName(nameList[i].strip())
    
    totalRunners = 0
    print(Fore.BLUE)
    for runner in nameList:
        if runner is not None:
            print(runner.name)
            totalRunners += 1
    print(Fore.RESET)

    runnersAdded = 0
    if input(f"Add {race.dist} to these people ({totalRunners} runners)? (y/n) ").lower() == "y":
        print(Fore.BLUE)
        for runner in nameList:
            runner.addToFile(race, None)
        print(Fore.RESET)

    print(f"{runnersAdded} runners added.")

    FileHandler.addToHistory(race)


def summarySheet():
    points_list = []
    
    for name in os.listdir("Members"):
        print(name[:-4])
        f = open(os.path.join("Members", name), "r")
        fileLines = f.readlines()
        points = int(fileLines[2].strip()[6:])
        f.close()

        points_list.append((points, name[:-4]))

    points_list.sort(reverse=True)

    lines_to_write = []
    for number, name in points_list:
        if number != 0:
            lines_to_write.append(f"{name} - {number}\n")

    summary_sheet = open("Summary Sheet.txt", "w")
    summary_sheet.writelines(lines_to_write)


def backup():
    dateForFile = str(datetime.date.strftime(datetime.date.today(), "%d-%m-%Y"))

    if not os.path.exists(os.path.join("Backups", dateForFile)):
        os.makedirs(os.path.join("Backups", dateForFile))

    for file in os.listdir("Members"):
        open(os.path.join("Backups", dateForFile, file), "w").close()
        shutil.copy(os.path.join("Members", file), 
                    os.path.join("Backups", dateForFile, file))
    
    open(os.path.join("Backups", dateForFile, "1 parkruns.txt"), "w").close()
    shutil.copy("Parkruns/parkruns.txt", 
                os.path.join("Backups", dateForFile, "1 parkruns.txt"))
    
    summarySheet()
    open(os.path.join("Backups", dateForFile, "2 Summary Sheet.txt"), "w").close()
    shutil.copy("Summary Sheet.txt", os.path.join("Backups", dateForFile, "2 Summary Sheet.txt"))
      
    print(f"Backup made for {dateForFile}")

mainloop()
