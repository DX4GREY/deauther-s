#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from logging import err, ok, warn
from colorama import Fore, Style, init
from utils import check_superuser, check_dependencies, validate_interface, cleanup_tmp_files
from attacks import start_deauth, start_beacon_flood
from scanner import run_airodump_scan, parse_airodump_csv, interactive_choose
from variables import SHORTCUT_PATH, FOLDER_PATH

init(autoreset=True)

def print_banner():
    print(Fore.RED + Style.BRIGHT + rf"""
    ▛▀▖ {Fore.RESET}Scanner{Fore.RED} ▐  ▌   {Fore.RESET}With{Fore.RED}    ▞▀▖
    ▌ ▌▞▀▖▝▀▖▌ ▌▜▀ ▛▀▖▞▀▖▙▀▖▄▄▖▚▄ 
    ▌ ▌▛▀ ▞▀▌▌ ▌▐ ▖▌ ▌▛▀ ▌     ▖ ▌
    ▀▀ ▝▀▘▝▀▘▝▀▘ ▀ ▘ ▘▝▀▘▘     ▝▀ 
{Fore.RESET}      Deauther-S | Dx4 and JonX
""" + Style.RESET_ALL)

def uninstall_script():
    print_banner()
    # Uninstall all SHORTCUT_PATH and FOLDER_PATH
    if os.path.exists(SHORTCUT_PATH) and os.path.exists(FOLDER_PATH):
        try:
            os.remove(SHORTCUT_PATH)
            ok(f"Removed shortcut: {SHORTCUT_PATH}")
        except Exception as e:
            err(f"Failed to remove shortcut: {e}")
        
        try:
            subprocess.run(["rm", "-rf", FOLDER_PATH], check=True)
            ok(f"Removed folder: {FOLDER_PATH}")
        except Exception as e:
            err(f"Failed to remove folder: {e}")
        
        ok("Uninstallation complete.")
    else:
        warn("Deauther-s is not installed.")
    sys.exit(0)

def set_channel(iface, channel):
    subprocess.run(["iw", iface, "set", "channel", str(channel)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(description="Simple Deauth Tool by Dx4 and JonX")
    parser.add_argument("-i", "--iface", help="Wireless interface (ex: wlan0)")
    # New feature beacon flood
    parser.add_argument("-b", "--beacon", action="store_true", help="Enable beacon flood mode")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup temporary files and exit")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall the deauther shortcut")
    args = parser.parse_args()

    if args.uninstall:
        uninstall_script()

    print_banner()
    check_superuser()
    check_dependencies()
    
    if args.cleanup:
        cleanup_tmp_files()
        sys.exit(0)

    if not args.iface:
        parser.print_help()
        return
    
    if not validate_interface(args.iface):
        return

    if not args.beacon:
        csv_file = run_airodump_scan(args.iface)
        aps = parse_airodump_csv(csv_file)

        if not aps:
            err(f"No APs found in scan!")
            return

        target_bssid, channel, _, _, = interactive_choose(aps)
        bssid = target_bssid

        start_deauth(bssid, channel, args.iface)
    else:
        start_beacon_flood(args.iface)

if __name__ == "__main__":
    main()