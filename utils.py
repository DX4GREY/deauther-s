from logging import err, ok, warn, info, input_field
import os
import sys
import subprocess
import shutil
from variables import REQUIRED_CMDS

def check_superuser():
    """Return True if running as root, otherwise exit program."""
    if os.geteuid() != 0:
        err("This tool must be run as root!")
        sys.exit(1)
    return True

def cleanup_tmp_files(prefix="deauther"):
    tmp_path = "/tmp"

    try:
        entries = os.listdir(tmp_path)
    except Exception as e:
        err(f"Failed to list /tmp: {e}")
        return

    for name in entries:
        if not name.startswith(prefix):
            continue

        path = os.path.join(tmp_path, name)

        try:
            if os.path.isdir(path):
                ok(f"Removing temporary folder: {path}")
                shutil.rmtree(path)
            else:
                ok(f"Removing temporary file: {path}")
                os.remove(path)

        except Exception as e:
            err(f"Failed to remove {path}: {e}")

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
def check_monitor_mode(iface):
    """Check if the specified interface is in monitor mode."""
    try:
        result = subprocess.run(["iw", iface, "info"], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if "type" in line:
                if "monitor" in line:
                    return True
                else:
                    return False
        return False
    except subprocess.CalledProcessError:
        err(f"Failed to get info for interface {iface}")
        sys.exit(1)

def start_monitor_mode(iface):
    """Set the specified interface to monitor mode."""
    info(f"Setting interface {iface} to monitor mode...")
    try:
        subprocess.run(["ip", "link", "set", iface, "down"], check=True)
        subprocess.run(["iw", iface, "set", "monitor", "none"], check=True)
        subprocess.run(["ip", "link", "set", iface, "up"], check=True)
        ok(f"Interface {iface} is now in monitor mode.")
    except subprocess.CalledProcessError as e:
        err(f"Failed to set monitor mode on {iface}: {e}")
        sys.exit(1)
        
def set_channel(iface, channel):
    subprocess.run(["iw", iface, "set", "channel", str(channel)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)