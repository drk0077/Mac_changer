#!/usr/bin/python3

import subprocess
import argparse
import re
import os
import sys


def validate_mac_address(mac):
    # new mac validation
    mac_pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"

    if re.match(mac_pattern, args.new_mac):
        return True
    else:
        return False

def check_root_privilege():
    if os.geteuid() != 0:
        print("[-] the script requires root user privilege, try using sudo before the script...")
        sys.exit(1)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="add the interface")
    parser.add_argument("-d", "--destination", dest="new_mac", help="add the new mac-address")
    return parser.parse_args()

def mac_change(inter, mac):
    try:
        subprocess.run(["ifconfig", inter, "down"], check=True)
        subprocess.run(["ifconfig", inter, "hw", "ether", mac], check=True)
        subprocess.run(["ifconfig", inter, "up"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[-] Error: Failed to change MAC address on interface {inter}. Please check if the interface is correct and you have sufficient permissions.")
    except FileNotFoundError:
        print( "[-] Error: 'ifconfig' command not found. Please install 'net-tools' or use the 'ip' command as an alternative.")
    except PermissionError:
        print("[-] Error: Insufficient permissions. Try running the script with 'sudo' or as root.")

check_root_privilege()
args = get_arguments()
if validate_mac_address(args.new_mac):
    new_mac = args.new_mac
    interface = args.interface
    print(f"[+] changing {interface} mac to {new_mac}.....")
    mac_change(interface, new_mac)

else:
    print("[-] Incorrect mac-address entered.... ")
