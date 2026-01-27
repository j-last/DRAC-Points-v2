
import time
import requests
from bs4 import BeautifulSoup as bs


class WebScraper:

    def getTotalRaceTimingResults(url:str) -> dict[str:time]:
        """Web scrapes all dereham runners AC results from a totalracetiming website.
        Returns a dictionary with entries in the form {runnerName : runnerTime}
        """
        race_runners = {}

        page = requests.get(url)
        soup = bs(page.content, "html.parser")
        runners = soup.find("tbody") # gets all 

        for runner in runners:
            runnerstring = runner.decode_contents()
            if "<td>Dereham Runners AC</td>" in runnerstring:
                runnerstring = runnerstring.split("<td")
                name = (runnerstring[2][1:-5] + " " + runnerstring[3][1:-5]).upper()
                raceTime = time.strptime(runnerstring[-2][2:-8], "%H:%M:%S")

                race_runners[name] = raceTime
        
        return race_runners
    

    def getParkrunners(web_text:str) -> list[str]:
        """Searches through the text to find all Dereham Runenrs who did parkrun,
        and returns a list of these names."""
        endindex = web_text.find("Dereham Runners AC")
        runners = []

        while endindex != -1:
            index = endindex
            spacesfound = 0
            while spacesfound != 2:
                index -= 1
                if web_text[index] == "	":
                    spacesfound += 1
            name = web_text[index:endindex].strip()
            name = name.split(" ")
            if len(name) >= 2:
                newname = name[0]
                for i in range(1, len(name)):
                    name[i] = name[i].upper()
                    newname += " " + name[i]
                name = newname
                runners.append(name)
            web_text = web_text[endindex + 1 :]
            endindex = web_text.find("Dereham Runners AC")

        return runners
    