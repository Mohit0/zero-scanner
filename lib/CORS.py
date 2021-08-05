#tested on 
import requests
import sys


def CORS(url):
    hearders = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
                'Origin':'testing.for.cors.com'}
    res = requests.get(url, headers=hearders)
    if res.status_code == 200:
        print("200 Found on URL")
        head = res.headers.__str__().lower()
        if 'access-control-allow-origin' in head:
            if res.headers['Access-Control-Allow-Origin'] == '*':
                print("Wild Card Used for CORS")
            elif 'testing.for.cors.com' in res.headers['Access-Control-Allow-Origin']:
                print ("CORS Exploitable")
            else: print('not vulnerable')



domain = sys.argv[1]
CORS(domain)