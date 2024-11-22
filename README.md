# SecureScan-UM
A Python script designed to scan websites using the "Ultimate Member" WordPress plugin for known vulnerabilities.
# Features
Detects if the "Ultimate Member" plugin is installed.
Extracts security tokens (nonce).
Identifies directory IDs required for potential exploitation.
Provides guidance for using SQLMap to test further vulnerabilities.

# Installation
1. Prerequisites:
Ensure Python 3.8 or higher is installed on your system.
# Install Required Libraries:
Run the following command to install necessary libraries:

## Usage:
To set up and run the scanner, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mo3awya1/SecureScan-UM
   cd WP-UM-Vuln-Scanner
   apt install dos2unix
   chmod +x setup.sh
   dos2unix setup.sh
   ./setup.sh
   python3 scanner.py -f targets.txt

## Examples
![Nature View](https://i.imgur.com/Uoe1Bys.png)
