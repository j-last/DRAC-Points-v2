
from colorama import Fore


class Printer:

    @staticmethod
    def white(msg:str, end="\n\n") -> None:
        """Prints white text to the terminal.
        """
        print(Fore.RESET + msg, end=end)

    @staticmethod
    def red(msg:str, end="\n\n") -> None:
        """Prints red text to the terminal.
        """
        print(Fore.RED + msg + Fore.RESET, end=end)

    @staticmethod
    def blue(msg:str, end="\n\n") -> None:
        """Prints blue text to the terminal.
        """
        print(Fore.BLUE + msg + Fore.RESET, end=end)

    @staticmethod 
    def green(msg:str, end="\n\n") -> None:
        """Prints green text to the terminal.
        """
        print(Fore.GREEN + msg + Fore.RESET, end=end)

    @staticmethod
    def yellow(msg:str, end="\n\n") -> None:
        """Prints yellow text to the terminal.
        """
        print(Fore.YELLOW + msg + Fore.RESET, end=end)

    @staticmethod
    def cyan(msg:str, end="\n\n") -> None:
        """Prints cyan text to the terminal.
        """
        print(Fore.CYAN + msg + Fore.RESET, end=end)
