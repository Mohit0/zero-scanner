

import requests
import sys

def HSTS(url):
    res = requests.get(url)
    if(res.status_code == 200):
        head = (res.headers).__str__().lower()
        if "strict-transport-security" not in head:
            print("No HSTS Header Found")
        #else:
         #   print(res.headers[Strict-Transport-Security])
            
domain = sys.argv[1]
url = ('https://' + domain).__str__().rstrip('\n')
#fun(url)