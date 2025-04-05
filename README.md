## **DEAUTHER-S by Dx4 & JonX**

A simple Python tool for performing **WiFi Deauthentication Attacks** using `aireplay-ng`.  
Supports interfaces with packet injection and monitor mode capabilities.

---

### **Features**
- Automatically detects the channel of the target BSSID  
- Automatically switches the interface to monitor mode  
- Continuous deauth attack until user stops (CTRL+C)  
- Can be run from anywhere via `deauther-s` command  
- Includes uninstall option: `deauther-s --uninstall`

---

### **Dependencies**
Required tools:
- `iw`
- `aireplay-ng` (from `aircrack-ng`)
- `ip`

To install dependencies:
```bash
sudo apt install aircrack-ng wireless-tools iproute2
```

---

### **Installation**
**1. Clone the repository**
```bash
git clone https://github.com/DX4GREY/deauther-s
cd deauther-s
```

**2. Run the installer**
```bash
sudo ./install.sh
```

The installer will:
- Check and verify dependencies
- Copy the main script to `/usr/local/bin` as `deauther-s`
- Make it globally executable from the terminal

---

### **Usage**
Example:
```bash
sudo deauther-s -i wlan0 -b 00:11:22:33:44:55
```

- `-i` = Wireless interface (e.g., wlan0)
- `-b` = Target BSSID (MAC address of the target WiFi)

---

### **Uninstall**
To remove the installed script:
```bash
sudo deauther-s --uninstall
```

This will only remove the script, not the dependencies.

---

### **Disclaimer**
**This tool is intended for educational and authorized testing purposes only. Do not use it on networks you do not own or have permission to test. You are fully responsible for your actions.**
!