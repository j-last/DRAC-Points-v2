
import os


for file in os.listdir("Members"):
    if file.count(" ") != 1:
        print(file)