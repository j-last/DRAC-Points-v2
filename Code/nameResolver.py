

import os

from Code.FileHandler import FileHandler
from Code.Printer import Printer
from Code.Runner import Runner


class NameResolver:
    
    @staticmethod
    def getRunnerFromUser() -> Runner:
        """Continually asks the user for a runner's name until it can be resolved to someone who exists or a new file is created.
        Returns None if the user enters nothing.
        """
        while True:
            name = input("Runner Name: ").upper()
            if name == "": return None
            
            if Runner.exists(name): 
                return Runner(name)
            
            runner = NameResolver.resolveName(name)
            if runner is not None:
                return runner

            runner = NameResolver.couldntResolve(name)
            if runner is not None:
                return runner
    
    
    @staticmethod
    def getRunnerFromName(name:str) -> Runner:
        if Runner.exists(name):
            return Runner(name)
        
        runner = NameResolver.resolveName(name)
        if runner is not None:
            return runner

        runner = NameResolver.couldntResolve(name)
        if runner is not None:
            return runner
        
        
    @staticmethod
    def resolveName(name:str):
        """Attempts to match a partial name to a file.
        Returns the name if it was successful, otherwise None.
        """
        if name.count(" ") != 1:
            return
        firstName, lastName = name.split()
        # Goes through files, seeing if any are an exact match 
        # or match the first 3 characters of the first name and the entire surname
        names = os.listdir("Members")
        for i in range(len(names), 0, -1):
            fileFirstName, fileLastName = names[i][:-4].split()
            if lastName != fileLastName: 
                names.remove(i)
                continue
            if firstName[:2] != fileFirstName[:2]:
                names.remove(i)
            
        if len(names) == 1:
            Printer.yellow(f"{name} -> {names[0][:-4]}")
            return Runner(names[0][:-4])
        else: 
            return
    

    @staticmethod
    def couldntResolve(name):
        print(f"'{name}' could not be resolved to a member\n    'c' - create a file\n    'n' - type in their file name")
        response = input().lower()

        if response == 'c':
            name = FileHandler.createFile()
            if name is not None:
                return Runner(name)
            
        
        elif response == 'n':
            runner = NameResolver.getRunnerFromUser()
            if runner is not None:
                return runner

