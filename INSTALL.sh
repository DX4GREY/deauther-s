#!/bin/bash

echo -e "\033[1;32m[*]\033[0m Installing Deauther-S by Dx4 & JonX..."

# Cek user root
if [[ $EUID -ne 0 ]]; then
   echo -e "\033[1;31m[!]\033[0m Please run as root"
   exit 1
fi

# Daftar dependencies
REQUIRED_CMDS=("iw" "aireplay-ng" "ip" "python3" "pip3")

# Install missing system dependencies
for cmd in "${REQUIRED_CMDS[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        echo -e "\033[1;33m[!]\033[0m Missing: $cmd. Installing..."
        apt install -y "$cmd"
    fi
done

# Install Python dependency
if ! python3 -c "import colorama" &> /dev/null; then
    echo -e "\033[1;33m[!]\033[0m Installing Python package: colorama"
    pip3 install colorama
fi

# Path skrip Python
SCRIPT_PATH="$(realpath deauth.py)"

# Buat shortcut command di /usr/local/bin
ln -sf "$SCRIPT_PATH" /usr/local/bin/deauther-s
chmod +x "$SCRIPT_PATH"

echo -e "\033[1;32m[+]\033[0m Installation complete!"
echo -e "\033[1;32m[+]\033[0m Now you can run: \033[1;37mdeauther -i wlan0 -b <BSSID>\033[0m"