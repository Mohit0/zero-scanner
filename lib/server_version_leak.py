import requests
import sys


def version_leak(url):
    hearders = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
                'Origin':'testing.for.cors.com'}
    res = requests.get(url, headers=hearders)
    if res.status_code == 200:
        print("200 Found on URL")
        head = res.headers.__str__().lower()
        if 'server' in head:
            s = res.headers['server']
            if any(char.isdigit() for char in s):
                print("Server Version Leakage Identified VERSION : " + res.headers['server'])

domain = sys.argv[1]
version_leak(domain)