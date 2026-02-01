

import os

from colorama import Fore

from Code.FileHandler import FileHandler
from Code.Printer import Printer
from Code.Runner import Runner


class NameResolver:
    
    @staticmethod
    def getRunnerFromUser() -> Runner:
        """Continually asks the user for a runner's name until it can be resolved to someone who exists or a new file is created.
        Returns a Runner object for the runner if it was successful.
        Returns None otherwise.
        """
        while True:
            name = input("Runner Name: ").upper()
            if name == "": return ""
            
            return NameResolver.getRunnerFromName(name)
    
    
    @staticmethod
    def getRunnerFromName(name:str) -> Runner:
        """Attempts to resolve the name of a runner to a file that exists.
        Returns a Runner object for the runner if it was successful.
        Returns None otherwise.
        """
        name = name.upper()
        if name.count(" ") > 1:
            name = name.split()[0] + " " + name.split()[2]
        if Runner.exists(name):
            return Runner(name)
        
        runner = NameResolver.resolveName(name)
        if runner is not None:
            return runner

        runner = NameResolver.couldntResolve(name)
        if runner is not None:
            return runner
        
        
    @staticmethod
    def resolveName(name:str) -> Runner:
        """Attempts to match a partial name to a file.
        Returns a Runner object for the runner if it was successful.
        Returns None otherwise.
        """
        if name.count(" ") != 1:
            return
        firstName, lastName = name.split()
        # Goes through files, seeing if any are an exact match 
        # or match the first 3 characters of the first name and the entire surname
        for j in range(2):
            names = os.listdir("Members")
            for i in range(len(names)-1, -1, -1):
                fileFirstName, fileLastName = names[i][:-4].split()
                if j == 0 and fileFirstName[:len(firstName)] == firstName and fileLastName[:len(lastName)] == lastName:
                    continue
                elif j == 1 and firstName[:2] == fileFirstName[:2] and lastName == fileLastName: 
                    continue
                names.pop(i)
            if len(names) == 1:
                Printer.yellow(f"{name} -> {names[0][:-4]}")
                return Runner(names[0][:-4])
        return
    

    @staticmethod
    def couldntResolve(name:str) -> Runner:
        """Prompts the user to either create a file or type in the actual file name if a name could not be resolved to a file.
        Returns a Runner object for the runner if it was successful.
        Returns None otherwise.
        """
        Printer.red(f"'{name}' could not be resolved to a member\n    {Fore.RESET}'c' - create a file\n    'n' - type in their file name\n    type nothing and press enter to do nothing")
        response = input().lower()

        if response == 'c':
            name = FileHandler.createFile()
            if name is not None:
                return Runner(name)
            
        elif response == 'n':
            return NameResolver.getRunnerFromUser()
        

    @staticmethod
    def capitalise(name:str):
        """Takes a name and capitalises it appropriately
        """
        name = list(name.lower())
        name[0] = name[0].upper()
        for i, letter in enumerate(name):
            if letter in [" ", "-"]:
                name[i+1] = name[i+1].upper()

        strName = ""
        for letter in name:
            strName += letter

        return strName


