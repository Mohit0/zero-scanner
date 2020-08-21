#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from urllib.parse import urlparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
from termcolor import colored
import tldextract
import os
import json


def check(url):
    hearders = {'Host': 'HackeR.CoM', 'X-Forwarded-Host':'HackeR.CoM'}
    try:
        res = requests.get(url, headers=hearders, allow_redirects=False, verify=False, timeout=(5, 27)) 
        #print(colored("Found " + res.status_code.__str__() + " Response Code", "green"))
    except Exception as e:
        print(e)
        print("\n")
    
    if res.status_code == 302 or res.status_code == 301:
        if "HackeR.CoM" in res.headers['Location'] or "hacker.com" in res.headers['Location']:
            print(colored("\tVulnerable to Host Header Injection\n\n", "red"))
            print(colored("Response Headers: ", "green"))
            print(json.dumps(dict(res.headers), sort_keys=True, indent=4))

    elif res.status_code == 200:
        if "HackeR.CoM" in res.content.__str__() or "hacker.com" in res.content.__str__():
            print(colored("\tVulnerable to Host Header Injection with Web Cache Poisoning\n\n","red")) 
    

def runner(domain):
    print(colored("Checking Host Header Injection\n", "green"))
    i=0
    payloads =  [" " , "?host_header=Host" , "?host_header=X-Forwarded-Host"]
    for payload in payloads:
        #print(colored(domain + payload, "green"))
        check(domain + payload)
    print("\n")




