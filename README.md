# WiFi Deauther

> **Disclaimer:**  
> **WARNING:** This tool is for educational purposes and authorized security testing only.  
> **Unauthorized use on networks without explicit permission is illegal.**  
> Use at your own risk.

## Overview

The **WiFi Deauth Tool** is a Python-based utility that provides several methods to perform WiFi deauthentication attacks. It leverages external tools such as `aircrack-ng` (which includes `airmon-ng`, `airodump-ng`, and `aireplay-ng`), `mdk4`, and `iw` to interact with wireless interfaces. This tool is designed for use in authorized penetration testing and network security research.

## Features

- **Interface Scanning & Selection:**  
  Lists available wireless interfaces (using `iw dev`) and allows you to select one.

- **Monitor Mode Management:**  
  Automatically enables monitor mode (using `airmon-ng`) on the selected interface and ensures that monitor mode is stopped upon exit or termination.

- **Attack Options:**
  - **Scan for Networks:** Launches `airodump-ng` to discover nearby WiFi networks.
  - **Deauth a Single Network:** Uses `aireplay-ng` to deauthenticate a specific network by BSSID.
  - **Deauth Multiple Networks:** Launches concurrent deauthentication attacks on multiple networks.
  - **Deauth All Networks in Range:** Uses `mdk4` to send deauthentication packets to all networks in range.

- **Enhanced Logging:**  
  Implements colorful and detailed logging via the Python package `coloredlogs` (with logs also written to `WIFI-Deauther.log`).

- **Signal Handling:**  
  Gracefully handles termination signals (e.g., Ctrl+C) to ensure proper cleanup (disabling monitor mode).

## Installation

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/PARIKAKUGOD1/WIFI-Deauther.git
cd WIFI-Deauther
```

### 2. Install System Dependencies

This tool depends on several external tools. For Debian-based systems (e.g., Ubuntu, Kali Linux), you can install them using the provided shell script.

#### Using the Provided Shell Script

Make the installation script executable and run it as root:

```bash
chmod +x install_requirements.sh
sudo ./install_requirements.sh
```

This script installs the following packages:
- **python3-coloredlogs** – For improved Python logging output.
- **mdk4** – For deauthentication of all networks in range.
- **iw** – For listing wireless interfaces.
- **aircrack-ng** – Which includes `airmon-ng`, `airodump-ng`, and `aireplay-ng`.

#### Alternatively, Manual Installation

If you prefer to install the dependencies manually, run:

```bash
sudo apt update
sudo apt install -y python3-coloredlogs mdk4 iw aircrack-ng
```

### 3. Verify Your Python Environment

Ensure you are running Python 3. This tool is designed to work with Python 3.

### 4. Usage

1. **Run the Tool as Root:**

   Since the tool manipulates network interfaces, it must be run with root privileges:

   ```bash
   sudo python3 WIFI-Deauther.py
   ```

2. **Select the Wireless Interface:**

   The tool will list all available wireless interfaces. Enter the number corresponding to the interface you wish to use.

3. **Choose an Attack Option:**

   An interactive menu will be presented with the following options:
   - **Scan for Networks:** Launches `airodump-ng` to scan for available WiFi networks.
   - **Deauth a Single Network:** Prompts you to enter a target network's BSSID for a deauthentication attack.
   - **Deauth Multiple Networks:** Prompts you to enter multiple BSSIDs (comma-separated) to attack concurrently.
   - **Deauth All Networks in Range:** Uses `mdk4` to deauthenticate every network within range.
   - **Exit:** Stops monitor mode and exits the tool.

4. **Follow On-Screen Prompts:**

   Depending on your selection, follow the prompts to perform the desired action. Use `Ctrl+C` to interrupt long-running operations such as network scanning.

## Files in the Repository

- **WIFI-Deauther.py**  
  The main Python script containing the WiFi deauthentication tool.

- **install_requirements.sh**  
  A shell script to install all required system packages on Debian-based systems.

- **requirements.txt**  
  Provided for reference; the project now uses `python3-coloredlogs` for Python logging.

