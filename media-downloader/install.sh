#!/bin/bash

# ANSI color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN} Media Downloader Installation Script ${NC}"
echo -e "${GREEN}=====================================${NC}"
echo

# --- Check for Termux ---
if ! [ -x "$(command -v termux-setup-storage)" ]; then
  echo -e "${RED}Error: This script is designed for Termux. Please run it in a Termux environment.${NC}"
  exit 1
fi

# --- Request Storage Permission ---
echo -e "${YELLOW}Requesting storage access...${NC}"
termux-setup-storage
sleep 2

# --- Update and Upgrade Packages ---
echo -e "${YELLOW}Updating package lists...${NC}"
pkg update -y || { echo -e "${RED}Failed to update packages.${NC}"; exit 1; }
echo -e "${YELLOW}Upgrading installed packages...${NC}"
pkg upgrade -y || { echo -e "${RED}Failed to upgrade packages.${NC}"; exit 1; }

# --- Install Core Dependencies ---
echo -e "${YELLOW}Installing core dependencies: python, ffmpeg, aria2...${NC}"
pkg install python ffmpeg aria2 -y || { echo -e "${RED}Failed to install core dependencies.${NC}"; exit 1; }

# --- Install Termux API for notifications ---
echo -e "${YELLOW}Installing Termux API for notifications...${NC}"
pkg install termux-api -y || { echo -e "${RED}Failed to install Termux API package.${NC}"; exit 1; }

# --- Install Python Dependencies ---
echo -e "${YELLOW}Installing Python libraries: yt-dlp...${NC}"
pip install --upgrade pip
pip install yt-dlp || { echo -e "${RED}Failed to install yt-dlp via pip.${NC}"; exit 1; }

# --- Make the main script executable ---
echo -e "${YELLOW}Setting up executable permissions...${NC}"
chmod +x media-downloader

# --- Final Instructions ---
echo
echo -e "${GREEN}===================================${NC}"
echo -e "${GREEN}      Installation Complete!       ${NC}"
echo -e "${GREEN}===================================${NC}"
echo
echo -e "To run the script, use the command:"
echo -e "${YELLOW}./media-downloader${NC}"
echo
echo -e "A symlink will be created in your bin folder so you can run it from anywhere."
# Create symlink for global access
INSTALL_DIR=$(pwd)
if [ ! -d "$HOME/../usr/bin" ]; then
    echo -e "${RED}Could not find the bin directory to create a symlink.${NC}"
else
    ln -s "$INSTALL_DIR/media-downloader" "$HOME/../usr/bin/media-downloader"
    echo -e "You can now run the script by simply typing ${YELLOW}media-downloader${NC} from any directory."
fi
echo
