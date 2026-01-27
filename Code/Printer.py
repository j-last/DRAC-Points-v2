
from colorama import Fore


class Printer:

    @staticmethod
    def red(msg:str):
        print(Fore.RED + msg + Fore.RESET, end="\n\n")

    def blue(msg:str):
        print(Fore.BLUE + msg + Fore.RESET, end="\n\n")
    
    def green(msg:str):
        print(Fore.GREEN + msg + Fore.RESET, end="\n\n")

    def yellow(msg:str):
        print(Fore.YELLOW + msg + Fore.RESET, end="\n\n")