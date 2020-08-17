#   Usage: python3 XSS_scanner.py http://testphp.vulnweb.com/

import requests
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


 
#url = sys.argv[1]
#print(scan_xss(url))