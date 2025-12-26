def capitaliseName(runnerName:str) -> str:
    runnerName = runnerName.strip().lower()
    runnerName = list(runnerName)
    
    runnerName[0] = runnerName[0].upper()
    for i in range(len(runnerName)):
        if runnerName[i] in [" ", "-"]:
            runnerName[i+1] = runnerName[i+1].upper()
    
    capitalisedName = ""
    for char in runnerName: capitalisedName += char
    return capitalisedName