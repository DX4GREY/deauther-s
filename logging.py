import colorama
from colorama import Fore
colorama.init(autoreset=True)
def ok(msg):
    print(f"{Fore.GREEN}[+] {Fore.WHITE}{msg}")

def err(msg):
    print(f"{Fore.RED}[!] {Fore.WHITE}{msg}")

def warn(msg):
    print(f"{Fore.YELLOW}[!] {Fore.WHITE}{msg}")

def info(msg):
    print(f"{Fore.CYAN}[*] {Fore.WHITE}{msg}")

def input_field(msg):
    return input(f"{Fore.GREEN}[?] {Fore.WHITE}{msg}").strip()