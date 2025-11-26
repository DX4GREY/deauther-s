import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

def ok(*msg, **kwargs):
    print(Fore.GREEN + "[+] " + Style.RESET_ALL, end="")
    print(*msg, **kwargs)

def err(*msg, **kwargs):
    print(Fore.RED + "[!] " + Style.RESET_ALL, end="")
    print(*msg, **kwargs)

def warn(*msg, **kwargs):
    print(Fore.YELLOW + "[!] " + Style.RESET_ALL, end="")
    print(*msg, **kwargs)

def info(*msg, **kwargs):
    print(Fore.CYAN + "[*] " + Style.RESET_ALL, end="")
    print(*msg, **kwargs)

def input_field(msg, **kwargs):
    return input(Fore.GREEN + "[?] " + Style.RESET_ALL + msg, **kwargs).strip()
