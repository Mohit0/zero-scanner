import sys
import os
from termcolor import colored


def cves_check(url,port_num):
    print(colored("Scanning For Options Bleed. ", "green"))
    cmd = "curl -sI -X OPTIONS https://" + url + ":" + port_num
    res = os.popen(cmd)
    output = res.read()
    output = output.__str__()
    #print(output)
    for line in output.splitlines():
        if "allow" in line or "Allow" in line:
            print("\tMethods Server " + line )
    print(colored("\tNot Vulnerable to Options Bleed.\n", "green"))

    print(colored("Scanning For CVE-2020-5902", "green"))
    cmd = "nmap -Pn -p " + port_num + " --script http-vuln-cve2020-5902 " + url
    res = os.popen(cmd)
    output = res.read()
    if "Host is vulnerable to CVE-2020-5902" in output or "VULNERABLE" in output:
        print(colored("\tVulnerable to CVE-2020-5902 CRITICAL ISSUE. \n Please find the Vulnerable URL below", "red"))
        print(colored(url + "/tmui/login.jsp/..;/tmui/locallb/workspace/fileRead.jsp?fileName=/etc/passwd", "red"))
    else:
        print(colored("\tNot Vulnerable to CVE-2020-5902\n", "green"))

    # print("Scanning For Top Ports")
    # cmd = "nmap -Pn -p 21,22,25,53,80,110,443,445,3306,3389 " + url
    # res = os.popen(cmd)
    # for line in res:
    #     if "open" in line:
    #         print(line.strip('\n'))




#domain = sys.argv[1]
#cves_check(domain)