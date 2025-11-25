#!/bin/bash

echo -e "\033[1;32m[*]\033[0m Installing Deauther by Dx4 & JonX..."

# Check root
if [[ $EUID -ne 0 ]]; then
   echo -e "\033[1;31m[!]\033[0m Please run as root"
   exit 1
fi

# Check is valid installation directory
if [[ ! -f deauth.py ]]; then
    echo -e "\033[1;31m[!]\033[0m Please run this script from the root of the cloned repository."
    exit 1
fi

# Required system dependencies
REQUIRED_CMDS=("iw" "aircrack-ng" "ip" "mdk4" "xterm" "python3" "pip3")

echo -e "\033[1;34m[*]\033[0m Checking dependencies..."

for cmd in "${REQUIRED_CMDS[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        echo -e "\033[1;33m[!]\033[0m Missing: $cmd. Installing..."
        
        case "$cmd" in
            aircrack-ng)
                apt install -y aircrack-ng ;;
            ip)
                apt install -y iproute2 ;;
            pip3)
                apt install -y python3-pip ;;
            *)
                apt install -y "$cmd" ;;
        esac
    fi
done

# Install Python dependency
if ! python3 -c "import colorama" &> /dev/null; then
    echo -e "\033[1;33m[!]\033[0m Installing Python package: colorama"
    pip3 install colorama
fi

# Path to main Python script
FOLDER_PATH="$(pwd)"
SCRIPT_PATH="$FOLDER_PATH/deauth.py"
TARGET="/usr/local/bin/deauther-s"

echo
echo -e "\033[1;34m[*]\033[0m Choose installation method:"
echo -e "    \033[1;37m1)\033[0m Symlink (ln -s)  — auto updates when editing script"
echo -e "    \033[1;37m2)\033[0m Copy (install)   — standalone, safer for global use"
echo

read -p "$(echo -e '\033[1;32m[?]\033[0m Select option (1/2): ')" choice

case "$choice" in
    1)
        echo -e "\033[1;34m[*]\033[0m Creating symlink at $TARGET"
        ln -sf "$SCRIPT_PATH" "$TARGET"
        ;;
    2)
        echo -e "\033[1;34m[*]\033[0m Copying script to $TARGET"
        cp -r "$FOLDER_PATH" /usr/share/deauther-s
        echo -e "\033[1;34m[*]\033[0m Setting up executable..."
        ln -sf "/usr/share/deauther-s/deauth.py" "$TARGET"
        ;;
    *)
        echo -e "\033[1;31m[!]\033[0m Invalid choice. Aborting."
        exit 1
        ;;
esac

chmod +x "$TARGET"

echo
echo -e "\033[1;32m[+]\033[0m Installation complete!"
echo -e "\033[1;32m[+]\033[0m Use the tool with:"
echo -e "    \033[1;37msudo deauther-s -i wlan0\033[0m"
echo
echo -e "\033[1;36m[*]\033[0m Features enabled:"
echo -e "    - Auto scanner (airodump-ng via xterm)"
echo -e "    - Interactive AP selection"
echo -e "    - Attack engine selector (aireplay / mdk4)"
echo -e "    - Xterm-based attack window"
echo -e "    - Graceful exit and cleanup"
echo