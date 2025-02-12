# WiFi Deauth Tool

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
  Implements colorful and detailed logging via the Python package `coloredlogs` (with logs also written to `wifi_deauth.log`).

- **Signal Handling:**  
  Gracefully handles termination signals (e.g., Ctrl+C) to ensure proper cleanup (disabling monitor mode).

## Installation

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/<your-username>/wifi-deauth-tool.git
cd wifi-deauth-tool
