import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
import json
from urlextract import URLExtract
from progressbar import ProgressBar
pbar = ProgressBar()

liste = []

def fun(dom,a):
	r = requests.get(dom, verify=False)
	#print(r.status_code)
	#print(json.dumps(dict(r.headers)))
	# print(json.dumps(endpoint_data,sort_keys=False,indent=4))
	#print(r.content)
	extractor = URLExtract()
	links = extractor.find_urls(r.content.__str__())
	links = set(links)
	createlist(links,a)


def createlist(links,a):
	for link in links:
		if a in link:
			liste.append(link)


def run(a):
	print("Crawling the pages...")
	fun("https://" + a + "/", a)
	print(len(liste))
	for x in pbar(range(len(liste))):
		try:
			fun(liste[x],a)
			listed = list(dict.fromkeys(liste))
		except Exception as e:
			print(e)
	print("Writing links in a file")
	path = "scripts/output/" + a
	f = open( path ,"a+")
	for x in range(len(liste)):
		#print(liste[x].__str__())
		f.write(liste[x] + "\n")
	f.close()
	print("Writing to File Completed")

#a = sys.argv[1]
#run(a)