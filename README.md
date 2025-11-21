## **DEAUTHER by Dx4 & JonX**

A Python-based WiFi **Deauthentication Attack Tool** with automatic scanning, AP selection, and support for multiple attack engines.
Runs inside `xterm` with interactive menus for easy usage.

---

## ⭐ **Features**

* 🔍 **Automatic WiFi scanning** using `airodump-ng`
* 📡 **Interactive AP selection** (shows BSSID, RSSI, channel, SSID)
* 🔄 **Automatic channel setting** for selected target
* ⚙️ **Choose attack engine:**

  * `aireplay-ng` (classic, stable)
  * `mdk4` (strong, aggressive)
* 🖥️ **Attacks run inside xterm** (colored output + auto-close)
* 🚀 **Globally accessible** via `deauther` command
* 🧹 **Includes easy uninstaller:**

  ```bash
  sudo deauther --uninstall
  ```

---

## 📦 **Dependencies**

Required tools:

* `iw`
* `ip`
* `xterm`
* `aireplay-ng`
* `airodump-ng`
* `mdk4`

Install on Debian/Ubuntu/Kali:

```bash
sudo apt install aircrack-ng mdk4 xterm wireless-tools iproute2
```

---

## 📥 **Installation**

### **1. Clone repository**

```bash
git clone https://github.com/DX4GREY/deauther-s
cd deauther-s
```

### **2. Run installer**

```bash
sudo ./install.sh
```

Installer will:

* Check and verify required commands
* Copy main script to `/usr/local/bin/deauther`
* Make it globally executable
* Test environment compatibility

---

## 🕹️ **Usage**

### **Basic**

```bash
sudo deauther -i wlan0
```

This will:

1. Launch **airodump-ng** inside xterm
2. Save CSV results
3. Show a **list of detected APs**
4. Ask you to choose a target
5. Ask you to choose attack method (aireplay-ng or mdk4)
6. Launch the attack

---

## 🎯 **Attack Method Selection**

You will be prompted with:

```
----- Select Attack Method -----
1. aireplay-ng (classic, stable)
2. mdk4 (stronger, faster, more aggressive)
```

Choose **1** or **2** depending on your needs.

---

## ❌ **Uninstallation**

To remove the installed shortcut:

```bash
sudo deauther --uninstall
```

This only removes `/usr/local/bin/deauther`
(not the repository nor dependencies).

---

## ⚠️ **Disclaimer**

This tool is for **educational and authorized security testing only**.
Do **NOT** attack networks without explicit permission.
You are fully responsible for your actions.