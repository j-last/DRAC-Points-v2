import json
import os
import time
import datetime

# constants
timeFormat = "%H.%M.%S"
VALID_AGES = ["MU17", "M17-39", "M40-44", "M45-49", "M50-54", "M55-59", "M60-64", "M65+",
                 "WU17", "W17-34", "W35-39", "W40-44", "W45-49", "W50-54", "W55-59", "W60-64", "W65+"]





def calcPoints(raceTime, dist, ageCat):
    standards = open("Code/Standards.json")
    data = json.load(standards)
    standards.close()

    standards = data[ageCat][dist]

    points = 4
    for standardTime in standards:
        if raceTime <= time.strptime(standardTime, timeFormat):
            points += 1
    if points == 9: points += 1
    return points

