#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
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
import urllib.parse 

  #  COMMENT ADDED HERE

def general(url):
    if result.scheme == "https":
        ssl_socket_upgraded.runner(result.netloc)  
    hearders = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
                'Origin':'testing.for.cors.com'}
    print(colored("\nSending Requests to " + url,"green"))
    res = requests.get(url, headers=hearders,verify=False)
    #print(res.request.headers)
    #print(res.headers)
    if (res.status_code  > 300) and (res.status_code < 303):
        print("Redirection Found to" + res.headers['Location'])
    if res.status_code == 200:
        print(colored("200 Found on URL", "green"))
        head = res.headers.__str__().lower()
        if 'x-frame-options' in head or 'frame-option' in head:
            value = res.headers['X-Frame-Options']
            value = value.__str__().lower()
            if ("sameorigin" not in value) and ("deny" not in value):
                print(colored("X-Frame-Options Header " + "Currently set to: " + value , "yellow"))
        if 'x-frame-options' not in head or 'frame-option' not in head:
            print(colored("Vulnerable to Clickjacking Attack","red"))
        if "strict-transport-security" not in head:
            print(colored("No HSTS Header Found" , "red"))
        if 'access-control-allow-origin' in head:
            if res.headers['Access-Control-Allow-Origin'] == '*':
                print(colored("Wild Card Used for CORS" , "yellow"))
            elif 'testing.for.cors.com' in res.headers['Access-Control-Allow-Origin']:
                print(colored("CORS Exploitable", "red"))
        if 'server' in head:
            try: 
                var = res.headers['server']
                if any(char.isdigit() for char in var):
                    print(colored("Server Version Leakage Identified VERSION : " + res.headers['server'], "red"))
                else:
                    print(colored("Server Details identified : " + res.headers['server'], "yellow" ))
            except:
                pass
 
    

def standalone():
    try:
        host_header_injection.runner(result.netloc)    
    except Exception as e:
        print("Exception with host Header Injection:  ")
        print(e)

    try:
        if digit <= 3:
            http1_0test.runner(result.netloc)
        else:
            pass
    except Exception as e:
        print("Exception when sending request with HTTP/1.0:  ")
        print(e)
    try:
        popular_cve.cves_check(result.netloc)
    except Exception as e:
        print("Exception with Popular CVE script: ")
        print(e)

    try:
        aem.aemrunner(result.scheme, result.netloc)
    except Exception as e:
        print("Exception with AEM Script:  ")
        print(e)
    try:
        directory_listing.dir_listing_runner(dom)
    except Exception as e:
        print("Exception with Dir Listing Script:  ")
        print(e)
    
    
digit = 0   
dom = ""   
try: 
    print("USAGE:\n https://domain.com/path?query \n http://domain.com/path?query ")        
    url1 = input("Enter the URL/IP Address: ")
    for character in url1:
        if character.isdigit():
            digit = digit + 1
    if digit <= 3:
        result = urllib.parse.urlparse(url1)
        params = urllib.parse.parse_qsl(result.query)
        dom = result.scheme + "://" + result.netloc + result.path 
        i=0
        if result.query != "":
            dom = dom + "?"
            for par in params:
                i=i+1
                if len(params) == 1:
                    dom = dom + par[0] + "=" + par[1]
                elif len(params) == i:
                    dom = dom + par[0] + "=" + par[1] 
               	else:
                    dom = dom + par[0] + "=" + par[1] + "&"
    elif digit >= 4:
        print("This Version Do not support IP addess yet")
    try:
        general(dom)
        standalone() 
    except KeyboardInterrupt:
        print("Canceling script...")
        sys.exit(1)
except Exception as e:
    print("\n\nUsage :  python3 scanner_engine.py www.domain.com/url\n" + e.__str__() + "\n") 








