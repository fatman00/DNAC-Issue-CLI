#! /usr/bin/python

"""
bob
Use this to configure default setup on Eve-NG devices

pip freeze > requirements.txt
pip install -r requirements.txt
"""

__author__ = "Rasmus E"
__author_email__ = "fatman00hot@hotmail.com"
__copyright__ = "Copyright (c) 2020 Rasmus E"
__license__ = "MIT"

from pprint import pprint
#from datetime import datetime
from argparse import ArgumentParser
import sys
import time
#import requests
import getpass
import json
#import telnetlib
#import csv
#import re

import pandas as pd
# dnacentersdk kan be found here: https://github.com/cisco-en-programmability/dnacentersdk
from dnacentersdk import api

if __name__ == '__main__':
    parser = ArgumentParser(description='Select options.')
    # Input parameters
    # https://sandboxdnac.cisco.com:443
    # https://dcloud-dnac-ctf-inst-lon.cisco.com
    parser.add_argument('--host', type=str, default='https://sandboxdnac.cisco.com:443',
                        help="Hostname of DNAC to connect to")
    parser.add_argument('--username', type=str, default="admin",
                        help="username")
    parser.add_argument('--password', type=str, default="None",
                        help="password")
    parser.add_argument('--dryrun', action="store_true",
                        help="Only do a test run without and log details without changeing configuration")
    args = parser.parse_args()
    # Print the args if we want. :print(sys.argv[1:])
    if args.host == None:
        print("Hostname of the DNAC not defined")
        sys.exit(1)
    # If password not defined then ask for it.
    if args.password == None or args.password == "None":
        args.password = getpass.getpass(f"Type the password for {args.username}: ")

    print(f"{args.host} and username: {args.username} and password: *******")
    
    
    # Create a DNACenterAPI connection object;
    # it uses DNA Center sandbox URL, username and password, with DNA Center API version 2.2.3.3.
    # and requests to verify the server's TLS certificate with verify=True.
    dnac = api.DNACenterAPI(username=args.username,
                            password=args.password,
                            base_url=args.host,
                            version='2.2.3.3',
                            verify=False)


    print()
    print("Fetching the complete device list from Inventory...")
    print()
    devices = dnac.devices.get_device_list(role = "ACCESS")

    print(pd.DataFrame(json.loads(json.dumps(devices.response)), columns=["id", "hostname", "role"]))

    for device in devices.response:
        #print('{:20s} {} {} {}'.format(device.hostname, device.upTime, device.reachabilityStatus, device.errorDescription))
        print(device.id + ": "+device.role + ": "+ device.roleSource)
        dnac.devices.update_device_role(id = device.id, role = "DISTRIBUTION", roleSource = "MANUAL")
    # Find all issues that are pressent on the DNAC
    print()
    print()