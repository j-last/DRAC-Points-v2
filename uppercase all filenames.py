
import os

from Code.FileHandler import FileHandler


for runnerfile in os.listdir("Members"):
    fileLines = FileHandler.getFileLines(runnerfile[:-4])
    fileLines[0] = fileLines[0].upper()
    os.remove(os.path.join("Members", runnerfile))
    fd = os.open(f"Members\\{runnerfile[:-4].upper()}.txt", os.O_CREAT)
    os.close(fd)
    FileHandler.writeFileLines(runnerfile[:-4].upper(), fileLines)
    if fileLines[1].strip()[:-2] == "??":
        print(runnerfile)