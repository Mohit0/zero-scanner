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


sys.path.insert(1, 'lib')
import general
import ssl_socket_upgraded
import host_header_injection
import http1_0test
import popular_cve
import XSS_scanner
import aem


sys.path.insert(1, 'scripts')
import directory_listing



#   VARIABLES HERE
dom = ''
url = ''
path = '/'
port_num = 443
digit = 0



def exploiter():
    try:
        try:
            general.general("https://" + url)
            print(colored("Performing SSL checks.","green"))
            ssl_socket_upgraded.runner(dom,port_num)
        except Exception as e:
            print("Error: " + e.__str__())
            sys.exit(1)
        standalone(port_num.__str__())
    except KeyboardInterrupt:
        print("Canceling script...")
        sys.exit(1)



def standalone(port_num):
    try:
        #print("Passed Host Header")
        host_header_injection.runner(dom, port_num ,path)
    except Exception as e:
        print("Exception with host Header Injection:  ")
        print(e)
    try:
        if digit <= 3:
            #print("Passed Internal IP checks")
            http1_0test.runner(dom + ":" + port_num)
    except Exception as e:
        print("Exception when sending request with HTTP/1.0:  ")
        print(e)
    try:
        #print("Passed Popular CVEs checks")
        popular_cve.cves_check(dom,port_num)
    except Exception as e:
        print("Exception with Popular CVE script: ")
        print(e)
    try:
        print(colored("Performing quick validation for XSS.","green"))
        XSS_scanner.scan_xss("https://" + url)
        print("\n")
        #print("Passed XSS checks")
    except Exception as e:
        print("Exception with XSS scan script:  ")
        print(e)
    try:
        #aem.aemrunner(dom + ":" + port_num)
        print("Not vulnerable to AEM vulnerability")
    except Exception as e:
        print("Exception with AEM Script:  ")
        print(e)
    try:
        print("Directory Enumeration is commented out\n\n")
        #directory_listing.dir_listing_runner(dom + ":" + port_num)
    except Exception as e:
        print("Exception with Dir Listing Script:  ")
        print(e)


# URL FORMER
def url_former():
    global url, dom, port_num, digit, path
    for character in url:
        if character.isdigit():
            digit = digit + 1
    if digit <= 3:
        result = urlparse(url)
        dom = result.netloc
        path = result.path.__str__()
        url = result.netloc + ":" + port_num.__str__() + result.path
    elif digit >= 4:
        try: 
            url,port_num = url.split(":")
            dom = url
        except:
            dom = url
        url = url + ":" + port_num.__str__()
    print(colored("Host= " + dom + "\nPort Number= " + str(port_num) + "\nURL Formed = " + url + "\n", "blue"))
    try: 
        requests.get("https://" + url, verify=False, timeout=(10, 27))
        exploiter()
    except KeyboardInterrupt:
        print("Canceling script...")
    except Exception as e:
        print(e)
        print("\n")
        pass    




def option2():
    global url, dom, port_num
    try:
        print("\nUSAGE:\n https://domain.com/path \n 255.255.255.255\n")
        url = input("Enter the URL/IP Address: ")
        if url == "":
            print("No Input. Exiting...\n")
            sys.exit(1)
        url = url.__str__().rstrip('\n').rstrip(' ')
        port_num = input("Enter port(default 443): ")
        if port_num == '':
            port_num = 443
        else:
            port_num = int(port_num)
        print(colored("\nFetching Scripts and Running Scanner\n", "green"))
        url_former()
    except KeyboardInterrupt:
        print("Canceling script...")
        sys.exit(1)
    except Exception as e:
        print("\nUSAGE:\n domain.com/path?query \n 255.255.255.255 \nERROR : " + e.__str__() + "\n")



#   MAIN FUNCTION
if __name__ == '__main__':
    try:
        print("\n1. Read targets from file.")
        print("2. Continue with interactive terminal mode.")
        num = input("\nSelct an Option(1 or 2): ")
        if int(num) == 1:
            path = input("\nPlease provide the path to file: ")
            file = open(path.__str__().rstrip('\n'), "r")
            print("\n Fetching Scripts and Running Scanner\n\n")
            for target in file:
                url = target.__str__().rstrip('\n').rstrip(' ')
                url_former()
        if int(num) == 2:
            try:
                option2()
            except Exception as e:
                print(e)
                sys.exit(1)
        else:
            print("Invalid Input")
            sys.exit(1)
    except KeyboardInterrupt:
        print("Canceling script...")
    except Exception as e:
        print(e)












