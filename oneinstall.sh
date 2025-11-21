#!/bin/bash

echo -e "\033[1;32m[*]\033[0m Running Deauther One-Line Installer..."

# Pastikan script dijalankan sebagai root (karena install.sh butuh root)
if [[ $EUID -ne 0 ]]; then
   echo -e "\033[1;31m[!]\033[0m Please run using: sudo bash"
   exit 1
fi

TMP_DIR="/tmp/deauther-install-$(date +%s)"

echo -e "\033[1;34m[*]\033[0m Cloning repository into temporary directory..."
git clone https://github.com/DX4GREY/deauther-s "$TMP_DIR" >/dev/null 2>&1

if [[ $? -ne 0 ]]; then
    echo -e "\033[1;31m[!]\033[0m Failed to clone repository."
    exit 1
fi

cd "$TMP_DIR" || exit

echo -e "\033[1;34m[*]\033[0m Running installer..."

# Jalankan installer
INSTALL_PATH="/usr/local/bin/deauther-s"
bash install.sh

# Deteksi apakah user memilih symlink atau copy
if [[ -L $INSTALL_PATH ]]; then
    METHOD="symlink"
elif [[ -f $INSTALL_PATH ]]; then
    METHOD="copy"
else
    METHOD="unknown"
fi

echo -e "\033[1;34m[*]\033[0m Detected installation type: $METHOD"

# Jika hasil install adalah copy → hapus folder git clone
if [[ "$METHOD" == "copy" ]]; then
    echo -e "\033[1;33m[*]\033[0m Cleaning up installation directory (copy mode)..."
    rm -rf "$TMP_DIR"
else
    echo -e "\033[1;36m[*]\033[0m Keeping folder (symlink mode)."
fi