# **DEAUTHER-s**

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
* 🚀 **Globally accessible** via `deauther-s` command
* 🧹 **Includes easy uninstaller:**

  ```bash
  sudo deauther-s --uninstall
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

### 📥 **One-Line Installation**


**One-line installer:**

```
curl -sSL https://raw.githubusercontent.com/DX4GREY/deauther-s/master/oneinstall.sh -o /tmp/deauther-one.sh && sudo bash /tmp/deauther-one.sh && rm /tmp/deauther-one.sh
```
---

## 🕹️ **Usage**

### **Basic**

```bash
sudo deauther-s -i wlan0
```

## ❌ **Uninstallation**

To remove the installed shortcut:

```bash
sudo deauther-s --uninstall
```

This only removes 'deauther-s' resources
(not the repository nor dependencies).

---

## ⚠️ **Disclaimer**

This tool is for **educational and authorized security testing only**.
Do **NOT** attack networks without explicit permission.
You are fully responsible for your actions.