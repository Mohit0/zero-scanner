

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
from termcolor import colored


def check_dir_listing(url):
	hearders = {'headers':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}
	result = requests.get(url, headers = hearders, verify=False)
	#print(url)
	#print(result.status_code)
	if (result.status_code != 404) and (result.status_code != 302) and (result.status_code != 300) and (result.status_code != 301):
		if "not found" not in result.content.__str__().lower():
			print(colored('Predictable Resource Location: ' + url , "red" )) 
			if result.status_code == 200:
				# print('In Directory Listing Function')
				v1 = result.text
				v2 = v1[v1.find('<title>') + 7 : v1.find('</title>')]
				if 'index' in v2.__str__().lower():
					print(colored("Also Vulnerable to Directory Listing","red"))
	

def dir_listing_runner(domain):
	path = "scripts/payloads/common_directories.txt"
	#domain = sys.argv[1]
	i = 0
	file = open(path, "r")
	print("Check for Hidden Directories Running..")
	for url in file.readlines():
		url = ('https://' + domain + '/' + url).__str__().rstrip('\n')
		try: 
	
			check_dir_listing(url)
			url = url + '/'
			check_dir_listing(url)
		except Exception as e:
			i = i + 1	
			if i >= 2:
				print('Host seems down. Error: ' + e.__str__()) 
				exit()


#domain = sys.argv[1]
#dir_listing_runner(domain)
		