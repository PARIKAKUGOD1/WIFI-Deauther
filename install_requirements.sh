#!/bin/bash
# install_requirements.sh
# This script installs all required packages for the WiFi Deauth Tool.
# It is intended for Debian-based systems.
#
# Required packages:
#   - python3-coloredlogs
#   - mdk4
#   - iw
#   - aircrack-ng
#
# Run this script as root:
#   sudo ./install_requirements.sh

# Ensure the script is run as root.
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root: sudo ./install_requirements.sh"
    exit 1
fi

echo "Updating package list..."
apt update

echo "Installing required packages..."
apt install -y python3-coloredlogs mdk4 iw aircrack-ng

echo "Installation complete."
