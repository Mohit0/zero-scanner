import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from termcolor import colored
import json



def general(url):
    hearders = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
                'Origin': 'testing.for.cors.com'}
    print(colored("Sending Requests to Server :  " + url, "green"))
    print("\n")
    res = requests.get(url, headers=hearders, verify=False, timeout=(10, 27))
    print(colored("Found " + res.status_code.__str__() + " Response Code", "green"))
    #print(colored("Response Headers: ", "green"))
    #print(json.dumps(dict(res.headers), sort_keys=True, indent=4))
    #print("\n")
    if (res.status_code > 300) and (res.status_code < 303):
        print("Redirection Found to" + res.headers['Location'])
    if res.status_code:
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
