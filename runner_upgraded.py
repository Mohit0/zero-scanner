#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
from urllib.parse import urlparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys

sys.path.insert(1, 'lib')
import ssl_socket_upgraded
import popular_cve
import aem
import host_injection
import host_header_injection
import http1_0test
import tldextract

sys.path.insert(1, 'scripts')
import directory_listing
from termcolor import colored


#  COMMENT ADDED HERE

def general(url):
    ssl_socket_upgraded.runner(dom,port_num)
    hearders = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
                'Origin': 'testing.for.cors.com'}
    print(colored("\nSending Requests to Server :  " + url, "green"))
    res = requests.get(url, headers=hearders, verify=False)
    if (res.status_code > 300) and (res.status_code < 303):
        print("Redirection Found to" + res.headers['Location'])
    if res.status_code == 200:
        print(colored("200 Found on URL", "green"))
        head = res.headers.__str__().lower()
        if 'x-frame-options' in head or 'frame-option' in head:
            value = res.headers['X-Frame-Options']
            value = value.__str__().lower()
            if ("sameorigin" not in value) and ("deny" not in value):
                print(colored("X-Frame-Options Header " + "Currently set to: " + value, "yellow"))
        if 'x-frame-options' not in head or 'frame-option' not in head:
            print(colored("Vulnerable to Clickjacking Attack", "red"))
        if "strict-transport-security" not in head:
            print(colored("No HSTS Header Found", "red"))
        if 'access-control-allow-origin' in head:
            if res.headers['Access-Control-Allow-Origin'] == '*':
                print(colored("Wild Card Used for CORS", "yellow"))
            elif 'testing.for.cors.com' in res.headers['Access-Control-Allow-Origin']:
                print(colored("CORS Exploitable", "red"))
        if 'server' in head:
            try:
                var = res.headers['server']
                if any(char.isdigit() for char in var):
                    print(colored("Server Version Leakage Identified VERSION : " + res.headers['server'], "red"))
                else:
                    print(colored("Server Details identified : " + res.headers['server'], "yellow"))
            except:
                pass
        print("\n")


def standalone(port_num):
    try:
        host_header_injection.runner(dom + ":" + port_num)
    except Exception as e:
        print("Exception with host Header Injection:  ")
        print(e)
    try:
        if digit <= 3:
            http1_0test.runner(dom + ":" + port_num)
    except Exception as e:
        print("Exception when sending request with HTTP/1.0:  ")
        print(e)
    try:
        popular_cve.cves_check(dom,port_num)
    except Exception as e:
        print("Exception with Popular CVE script: ")
        print(e)
    try:
        aem.aemrunner(dom + ":" + port_num)
    except Exception as e:
        print("Exception with AEM Script:  ")
        print(e)
    try:
        directory_listing.dir_listing_runner(dom + ":" + port_num)
    except Exception as e:
        print("Exception with Dir Listing Script:  ")
        print(e)


if __name__ == '__main__':
    digit = 0
    dom = ''
    url = ''
    port_num = 443
    try:
        print("USAGE:\n https://domain.com/path \n 255.255.255.255 ")
        url = input("Enter the URL/IP Address: ")
        if url == "":
            print("No Input. Exiting...")
            sys.exit(1)
        url = url.__str__().rstrip('\n').rstrip(' ')
        port_num = input("Enter port(default 443): ")
        if port_num == '':
            port_num = 443
        else:
            port_num = int(port_num)
        for character in url:
            if character.isdigit():
                digit = digit + 1
        if digit <= 3: #if digit is less then URL parsing is done
            result = urlparse(url)
            dom = result.netloc
            url = result.netloc + ":" + port_num.__str__() + result.path
        elif digit >= 4: # if digit is more considering IP received
            dom = url
            url = url + ":" + port_num.__str__()
        print("\n Fetching Scripts and Running Scanner\n\n")
        try:
            try:
                general("https://" + url)
                #print("passed")
            except Exception as e:
                print("Error: " + e.__str__())
                sys.exit(1)
            standalone(port_num.__str__())
        except KeyboardInterrupt:
            print("Canceling script...")
            sys.exit(1)
    except Exception as e:
        print("\nUSAGE:\n domain.com/path?query \n 255.255.255.255:port \nERROR : " + e.__str__() + "\n")









