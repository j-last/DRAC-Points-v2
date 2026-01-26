

import os

from colorama import Fore
from Code.FileHandler import FileHandler
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
            return NameResolver.couldntResolve(name)
        firstName, lastName = name.split()
        for i in range(min(len(firstName), len(lastName)), 0, -1):
            name = ""
            for fileName in os.listdir("Members"):
                fileFirstName, fileLastName = fileName[:-4].split()
                if (fileFirstName[:i] == firstName[:i] and fileLastName[:i] == lastName[:i]):
                    if name != "":
                        return NameResolver.couldntResolve(f"{firstName} {lastName}")
                    name = fileName[:-4]
            if name != "":
                print(Fore.YELLOW)
                print(f"{firstName} {lastName} -> {name}")
                print(Fore.RESET)
                return Runner(name)
        if name == "": 
            return NameResolver.couldntResolve(f"{firstName} {lastName}")
        print(Fore.YELLOW)
        print(f"{firstName} {lastName} -> {name}")
        print(Fore.RESET)
        return Runner(name)
    

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

