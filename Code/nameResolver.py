

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

            create = input("This could not be resolved to a member. Create a file (y/n): ").lower()
            if create == "y":
                name = FileHandler.createFile()
                if name is not None:
                    return Runner(name)
    

    def getRunnerFromName(name:str) -> Runner:
        if Runner.exists(name):
            return Runner(name)
