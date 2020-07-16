# includes parsing an argument

import requests
import sys

def clickjack(url):
	# print ('Scanning: ' + url)
	hearders = {'headers':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}
	result = requests.get(url, headers = hearders)
	if result.status_code == 200:
		head = result.headers.__str__().lower()
		if 'x-frame-options' in head or 'frame-option' in head:
			# print ('Required X-Frame-Options Header Found')
			value = result.headers['X-Frame-Options']
			value = value.__str__().lower()
			if ("sameorigin" not in value) and ("deny" not in value):
				print("Might Vulnerable to Frameable Resource Vulnerability " + "Currently set to: " + value )
			else:
				print("Not Vulnerable to Framable Resource Vulnerability")
		else: 
			print("Vulnerable to Framable Resource Vulnerability (NO X-Frame-Options Header Found.)")



#url = sys.argv[1]
#url = 'https://' + url
#clickjack(url)

