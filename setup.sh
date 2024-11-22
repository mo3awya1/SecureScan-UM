#!/bin/bash

# 🛠️ Script for Setting Up WP-UM Vuln Scanner Environment 🌟

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'

# Welcome message
echo -e "${GREEN}🌟 Welcome to the WP-UM Vuln Scanner setup script! 🌟${RESET}"

# Step 1: Check Python installation
echo -e "${YELLOW}🔍 Checking Python installation...${RESET}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python is not installed. Please install Python 3.8 or higher to continue.${RESET}"
    exit 1
else
    echo -e "${GREEN}✅ Python is installed.${RESET}"
fi

# Step 2: Install required Python libraries
echo -e "${YELLOW}📦 Installing required Python libraries...${RESET}"
pip install --upgrade pip
pip install requests colorama pystyle
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Libraries installed successfully.${RESET}"
else
    echo -e "${RED}❌ Failed to install libraries. Please check your Python and pip installation.${RESET}"
    exit 1
fi

# Step 3: Create targets.txt file
echo -e "${YELLOW}📄 Checking for 'targets.txt' file...${RESET}"
if [ ! -f "targets.txt" ]; then
    echo -e "${YELLOW}📄 'targets.txt' not found. Creating a new file...${RESET}"
    cat <<EOL > targets.txt
https://example.com/
https://example2.com/
EOL
    echo -e "${GREEN}✅ 'targets.txt' created with example targets.${RESET}"
else
    echo -e "${GREEN}✅ 'targets.txt' already exists.${RESET}"
fi

# Step 4: Confirm scanner.py exists
echo -e "${YELLOW}📜 Checking for 'scanner.py' file...${RESET}"
if [ ! -f "scanner.py" ]; then
    echo -e "${RED}❌ 'scanner.py' is missing. Please ensure the script is in the same directory.${RESET}"
    exit 1
else
    echo -e "${GREEN}✅ 'scanner.py' found.${RESET}"
fi

# Final message
echo -e "${GREEN}🎉 Setup is complete! You can now run the scanner with the following command:${RESET}"
echo -e "${YELLOW}python3 scanner.py -f targets.txt${RESET}"
