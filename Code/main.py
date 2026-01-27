import datetime
import os
import shutil
import time
from Code.FileHandler import FileHandler
from Code.Printer import Printer
from Code.WebScraper import WebScraper
from Code.NameResolver import NameResolver
from Code.Race import Race

# constants
TIME_FORMAT = "%H.%M.%S"

# main code
def mainloop():
    """The main menu loop, asking the user to select a function from a list of possibilities.
    """
    while True:
        Printer.white("""------------------------------------------------------
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
        else: Printer.red("Not a valid option. Please try again.")


def urlRaceEntry():
    """Allows the user to enter a TotalRaceTiming link. All names are then resolved to a file name,
    displaying all results to the user, asking them to confirm before the results are added.
    """
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
        Printer.red("Something went wrong.")
        return

    # Resolve all names, creating a list of tuples in the form: (name that exists, their time)
    # Anyone not resolved added to a seperate list
    toAdd, notAdded = [], []
    for runnerName, raceTime in runnersAndTimes.items():
        runner = NameResolver.getRunnerFromName(runnerName)
        if runner is not None:
            toAdd.append((runner, raceTime))
        else:
            Printer.red(f"No result will be added for {runnerName}.")
            notAdded.append((runnerName, raceTime))
    
    # Display all results that will be added before they're added
    Printer.green("RESULTS:", "\n")
    for runner, raceTime in toAdd:
        Printer.blue(f"{runner.name} - {time.strftime(TIME_FORMAT, raceTime)}", "\n")
    answer = input(f"ADD THESE RESULTS? ({len(toAdd)} runners) (y/n) ")
    if answer.lower() == "y":
        # add the results
        for runner, raceTime in toAdd:
            runner.addToFile(race, raceTime)
            runnersAdded += 1
    else:
        Printer.red("No results added")
        return
    
    Printer.green(f"{runnersAdded} RUNNERS ADDED")

    # Display all not added results before exiting to main menu
    if len(notAdded) > 0:
        Printer.red("NOT ADDED: ", "\n")
        for runnerName, raceTime in notAdded:
            Printer.red(f"{runnerName} - {time.strftime(TIME_FORMAT, raceTime)}", "\n")

    FileHandler.addToHistory(race)
    

def addParkrunsAuto():
    """Allows the user to copy+paste a consolidated report from the parkrun website,
    summing up total parkruns in 'Parkruns/parkruns.txt' and adding points to juniors where applicable.
    """
    try: race :Race = Race("parkrun", "1")
    except ValueError: return
    Printer.red("If it starts asking you to create files, you can just ignore this (enter nothing) unless they are a junior.\n Alternatively, you can create a file for them to stop it asking again next time.")
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
            Printer.red(f"{name} is being ignored")
            continue

        if newlines.get(name) is not None:
            newlines[name] += 1
        else:
            newlines[name] = 1
        runners_added += 1
        Printer.white(f"{name.upper()} has now done {newlines[name]} parkruns.", end="\n")

        runner = NameResolver.getRunnerFromName(name)
        if runner is not None:
            if runner.ageCat in ["MU17", "WU17"]:
                runner.parkruns += 1
                runner.fileLines[3] = runner.fileLines[3] = "PARKRUNS: " + str(runner.parkruns) + "\n"
                FileHandler.writeFileLines(runner.name, runner.fileLines)
                if runner.parkruns < 10:
                    runner.addToFile(race, None)
                    continue
                Printer.cyan(f"{runner.name} has done more than 10 parkruns, no points added.")
                continue
            Printer.cyan(f"{runner.name} is not a junior, no points added.")
                

    FileHandler.writeParkruns(newlines)

    Printer.green(f"{runners_added} RUNNERS ADDED")

    FileHandler.addToHistory(race)


def manualRaceEntry():
    """Continually asks the user for a name (and a time if applicable) and adds this result to their file.
    """
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
        
    Printer.green(f"{runnersAdded} RUNNERS ADDED")
    FileHandler.addToHistory(race)


def listOfNames():
    """Allows the user to enter a list of names, which are then resolved to files before listing
    all names, asking the user to confirm all names have been resolved correctly before they are added.
    """
    try: race :Race = Race()
    except ValueError: return
    if not race.dist.isnumeric():
        Printer.red("A list of names can only be done for a race with a fixed amount of points.")
        return
    
    stringList = input("Enter a list of names, separated by commas (,):\n").upper()

    try:
        nameList = stringList.split(",")
        nameList[1]
    except:
        Printer.red("List is in an invalid format.")
        return
    
    for i in range(len(nameList)):
        nameList[i] = NameResolver.getRunnerFromName(nameList[i].strip())
    
    totalRunners = 0
    for runner in nameList:
        if runner is not None:
            Printer.blue(runner.name)
            totalRunners += 1

    runnersAdded = 0
    if input(f"Add {race.dist} point(s) to these people ({totalRunners} runners)? (y/n) ").lower() == "y":
        for runner in nameList:
            if runner is not None:
                runner.addToFile(race, None)

    Printer.green(f"{runnersAdded} runners added.")

    FileHandler.addToHistory(race)


def summarySheet():
    """Creates a summary sheet (a sheet of names in order of points) in Summary Sheet.txt
    """
    points_list = []
    
    for name in os.listdir("Members"):
        Printer.blue(name[:-4], end="\n")
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
    """Copies all files to a backups folder, including all members files, parkruns.txt and Summary Sheet.txt
    """
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
      
    Printer.green(f"Backup made for {dateForFile}")

mainloop()
