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
        print(colored("Found " + res.status_code.__str__() + " Response Code", "green"))
        print(colored("Response Headers: ", "green"))
        print(json.dumps(dict(res.headers), sort_keys=True, indent=4))
    except Exception as e:
        print(e)
        print("\n")
        return int(1) 
    
    if res.status_code == 302 or res.status_code == 301:
        if "HackeR.CoM" in res.headers['Location'] or "hacker.com" in res.headers['Location']:
            print(colored("\tVulnerable to Host Header Injection\n\n", "red"))
            #print(res.headers['Location'])
            return int(1)
        else:
            return int(0)

    elif res.status_code == 200:
        if "HackeR.CoM" in res.content.__str__() or "hacker.com" in res.content.__str__():
            print(colored("\tVulnerable to Host Header Injection with Web Cache Poisoning\n\n","red"))
            #print(res.content)
            return int(1)
        else:
            return int(0)
    else: 
        print("\n\n")

def runner(domain):
    i=0
    payloads =  [" " , "?host_header=Host" , "?host_header=X-Forwarded-Host"]
    for payload in payloads:
        i = check(domain + payload)
        if (i == 1):
            break


#   MAIN FUNCTION
if __name__ == '__main__':
    try:
        print("\n HOST HEADER INJECTION ON HTTP/HTTPS SERVICE ")
        path = input("\nPlease provide the path to file: ")
        file = open(path.__str__().rstrip('\n'), "r")
        print("\n")
        for target in file:
            url = target.__str__().rstrip('\n').rstrip(' ')
            result = urlparse(url)
            dom = result.netloc.__str__()
            path = result.path.__str__()
            print(colored(result.scheme.__str__() + "://" + dom + path , "blue"))
            print()
            runner(result.scheme.__str__() + "://" + dom + path)

    except KeyboardInterrupt:
        print("Canceling script...")
    except Exception as e:
        print(e)


