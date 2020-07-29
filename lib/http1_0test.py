

from http.client import HTTPConnection
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup
import urllib.parse
import sys


def local(domain):
    HTTPConnection._http_vsn = 10
    HTTPConnection._http_vsn_str = "HTTP/1.0"
    r = requests.get(domain, allow_redirects=False,verify=False)
    content = r.content
    soup = BeautifulSoup(content, "html.parser")
    for link in soup.find_all('a'):
        links = link.get('href')
        links = urllib.parse.urlparse(links)
        if "10." in links.netloc or "192.168." in links.netloc or "172.16." in links.netloc or "172.31." in links.netloc:
            #print("Internal IP detected: " + links.netloc.__str__()  + "  Sent request with HTTP/1.0 to " + domain)
            print(links.netloc)
            return links.netloc
        else:
            return 0 


def runner(dom):
    payloads = {"/images", "/js" , "/javascript" , "/css"}
    for payload in payloads:
        domain = "https://" + dom + payload
        #print(domain)
        try:
            r = local(domain)
            if r != 0:
                print("Internal IP detected: " + r.__str__()  + "  Sent request with HTTP/1.0 to " + domain + "\n")
                break
        except Exception as e:
            print(e)

#a = sys.argv[1]
#runner(a)

