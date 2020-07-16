
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
from termcolor import colored


def check(url):
    #print(url)
    hearders = {'Host': 'HackeR.CoM', 'X-Forwarded-Host':'HackeR.CoM'}
    try:
        res = requests.get(url, headers=hearders, allow_redirects=False, verify=False) 
        #print(res)
    except Exception as e:
        #print (e)
        return int(0) 
    
    if res.status_code == 302 or res.status_code == 301:
        if "HackeR.CoM" in res.headers['Location']:
            print(colored("\tVulnerable to Host Header Injection\n", "red"))
            #print(res.headers['Location'])
            return int(1)
        else:
            return int(0)
    elif res.status_code == 200:
        if "HackeR.CoM" in res.content.__str__():
            print(colored("\tVulnerable to Host Header Injection with Web Cache Poisoning\n","red"))
            #print(res.content)
            return int(1)
        else:
            return int(0)

def runner(domain):
    i=0
    print(colored("Validating Host Header Injection", "green"))
    payloads =  ["/" , "?host_header=X-Forwarded-Host" , "?host_header=Host"]
    for payload in payloads:
        i = check("https://" + domain + payload)
        if (i == 1):
            break
        i = check("http://" + domain + payload)
        if (i == 1):
            break
    if i == 0:
        print(colored("\tNot Vulnerable to Host Header Injection\n", "green"))


#domain = sys.argv[1].__str__().rstrip('\n')   
#runner(domain)