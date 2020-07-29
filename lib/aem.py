

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
from termcolor import colored

def aemscan(url):
    hearders = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    res = requests.get(url, headers=hearders ,verify=False)
    if res.status_code == 200:
        print(colored("200 on : " + url, "red"))
        return int(0)
    else:
        return int(1)

def aemrunner(domain):
	path = "lib/payloads/aem-paths.txt"
	file = open(path, "r")
	print(colored("AEM Scan Running..","green"))
	i = k = 0
	for url in file.readlines():
	    url = ("https://" + domain + url).__str__().rstrip('\n')
	    #print(url)
	    try:
	        j = aemscan(url)
	        if j == 0:
	                k = 1 
	        i = i + j
	        if i == 10 and k == 0:
	                print(colored("\tNot Vulnerable to AEM Vulnerability\n","green"))
	                break
	    except Exception as e:
	        print(e)

#domain = sys.argv[1]
#aemrunner(domain)