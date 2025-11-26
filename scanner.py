from logging import ok, err, warn, info, input_field
import os
import sys
import subprocess
import argparse
import csv
import re
from colorama import Fore, Style, init
init(autoreset=True)

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
        subprocess.run(["xterm", "-T", "APs Scan", "-geometry", "100x30-0-0", "-e", "bash", "-lc", cmd])
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

    # Hitung panjang SSID terpanjang
    max_ssid_len = max(len(ssid) if ssid else 3 for _, _, _, ssid in aps)
    max_ssid_len = max(max_ssid_len, 4)  # minimal panjang kolom

    # Lebar kolom
    col_no = 4
    col_ssid = max_ssid_len + 2
    col_ch = 6
    col_rssi = 8
    col_bssid = 20

    # Garis atas
    print("┌" + "─" * col_no + "┬" + "─" * col_ssid + "┬" + "─" * col_ch + "┬" +
        "─" * col_rssi + "┬" + "─" * col_bssid + "┐")

    # Header
    print(
        "│"
        f"{Fore.GREEN}{'No':<{col_no}}{Style.RESET_ALL}│"
        f"{Fore.GREEN}{'SSID':<{col_ssid}}{Style.RESET_ALL}│"
        f"{Fore.GREEN}{'CH':<{col_ch}}{Style.RESET_ALL}│"
        f"{Fore.GREEN}{'RSSI':<{col_rssi}}{Style.RESET_ALL}│"
        f"{Fore.GREEN}{'BSSID':<{col_bssid}}{Style.RESET_ALL}│"
    )

    # Garis tengah
    print("├" + "─" * col_no + "┼" + "─" * col_ssid + "┼" + "─" * col_ch + "┼" +
        "─" * col_rssi + "┼" + "─" * col_bssid + "┤")

    # Isi Tabel
    for i, (bssid, ch, rssi, ssid) in enumerate(aps, start=1):
        ssid_display = ssid if ssid else f"{Fore.RED}Err{Fore.WHITE}"

        print(
            "│"
            f"{Fore.YELLOW}{i:<{col_no}}{Style.RESET_ALL}│"
            f"{Fore.WHITE}{ssid_display:<{col_ssid}}{Style.RESET_ALL}│"
            f"{Fore.CYAN}{ch:<{col_ch}}{Style.RESET_ALL}│"
            f"{Fore.CYAN}{rssi:<{col_rssi}}{Style.RESET_ALL}│"
            f"{Fore.LIGHTCYAN_EX}{bssid:<{col_bssid}}{Style.RESET_ALL}│"
        )

    # Garis bawah
    print("└" + "─" * col_no + "┴" + "─" * col_ssid + "┴" + "─" * col_ch + "┴" +
        "─" * col_rssi + "┴" + "─" * col_bssid + "┘")

    choice = input_field("Select target: ")

    try:
        choice = int(choice) - 1
        if choice < 0 or choice >= len(aps):
            raise ValueError
    except ValueError:
        err(f"Invalid choice!")
        sys.exit(1)

    return aps[choice][0], aps[choice][1], aps[choice][2], aps[choice][3]