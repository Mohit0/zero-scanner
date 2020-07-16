


import socket
from urllib.parse import urlparse
import sys
from termcolor import colored

def httpGET(server, port, path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    request = "GET / HTTP/1.0\nHost: " + "hackertest.com" + "\nPath: " + path + "\n\n"
    s.connect((socket.gethostbyname(server),port))
    s.send(request.encode())
    response = s.recv(4096)
    result = response.decode()
    #print(result)
    if "hackertest" in result:
        print(colored("Vulnerable to Host Header Injection", "red"))


def hostcheck(url):
    #print (url)
    dom = urlparse(url)
    inport = 80
    httpGET(dom.netloc,inport,dom.path)



#  BELOW CODE IS NOT WORKING TILL NOW

def hostcheck1(url):
    digit = 0
    inport = 80
    for character in url.__str__():
        if character.isdigit():
            digit = digit + 1
    print(digit)
    if digit == 0:
        dom = urlparse(url)
        httpGET(dom.netloc,inport,dom.path)
    elif digit >= 4:
        forceinject(url)

def forceinject(url):
    flag = 0
    cmd = "" 
    res = os.popen(cmd)
    output = res.read()
    output = output.__str__()
    for line in output.splitlines():
        if "hackertest.com" in line:
            flag = 1
            break
    if flag == 1:
        print(colored("Vulnerable to Host Header Injection", "red"))
    elif flag == 0:
        print("Not Vulnerable to Host Header Injection")


#url = sys.argv[1]
#hostcheck(url)








