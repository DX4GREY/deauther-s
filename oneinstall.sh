#!/bin/bash
clear

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
FOLDER_PATH=/usr/share/deauther-s
bash install.sh

# Cek apakah FOLDER_PATH ada jika ada maka cek apakah deauther-s ada, jika duanya ada maka di anggap terinstall menggunakan copy
# Jika salah FOLDER_PATH tidak ada sedangkan INSTALL_PATH ada maka di anggap terinstall menggunakan symlink
if [[ -d "$FOLDER_PATH" && -f "$INSTALL_PATH" ]]; then
    METHOD="copy"
elif [[ ! -d "$FOLDER_PATH" && -f "$INSTALL_PATH" ]]; then
    METHOD="symlink"
else
    METHOD="not installed"
fi

echo -e "\033[1;34m[*]\033[0m Detected installation type: $METHOD"

# Jika hasil install adalah copy → hapus folder git clone
if [[ "$METHOD" == "copy" ]]; then
    echo -e "\033[1;33m[*]\033[0m Cleaning up installation directory (copy mode)..."
    rm -rf "$TMP_DIR"
else
    echo -e "\033[1;36m[*]\033[0m Keeping folder (symlink mode)."
    echo -e "\033[1;36m[*]\033[0m This folder is required for the symlink to function properly:"
    echo -e "\033[1;36m[*]\033[0m $TMP_DIR"
    echo -e "\033[1;36m[*]\033[0m You can edit the script directly here."
fi