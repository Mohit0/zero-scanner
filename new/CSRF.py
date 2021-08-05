#   Usage: python3 CSRF.py http://testphp.vulnweb.com/


import requests
from bs4 import BeautifulSoup as bs
import json 


def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
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


def scan_xss(url):
    forms = get_all_forms(url)
    print(f"Detected {len(forms)} forms.")
    for form in forms:
        form_details = get_form_details(form)
        print(json.dumps(dict(form_details), sort_keys=True, indent=4))



url = "http://testphp.vulnweb.com/"
scan_xss(url)