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
    # print(url)
    hearders = {'Host': 'HackeR.CoM', 'X-Forwarded-Host':'HackeR.CoM'}
    try:
        res = requests.get(url, headers=hearders, allow_redirects=False, verify=False, timeout=(5, 27)) 
    except Exception as e:
        print("Exception:" + str(e))
    
    if res.status_code == 302 or res.status_code == 301:
        if "HackeR.CoM" in res.headers['Location'] or "hacker.com" in res.headers['Location']:
            print(colored("\tVulnerable to Host Header Injection\n", "red"))
            #print(colored("Response Headers For Proof of Concept: ", "green"))
            print(json.dumps(dict(res.headers), sort_keys=True, indent=4))
            return int(1)
        else:
            return int(0)
    elif res.status_code == 200:
        if "HackeR.CoM" in res.content.__str__() or "hacker.com" in res.content.__str__():
            print(colored("\tVulnerable to Host Header Injection with Web Cache Poisoning\n\n","red")) 
            return int(1)
        else:
            return int(0)

def runner(domain):
    print(colored("Checking Host Header Injection", "green"))
    i=0
    payloads =  ["" , "?host_header=Host" , "?host_header=X-Forwarded-Host"]
    for payload in payloads:
        #print(colored(domain + payload, "green"))
        i = check(domain + payload)
        if (i == 1):
            break




