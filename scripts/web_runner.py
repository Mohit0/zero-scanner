#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from urllib.parse import urlparse
sys.path.insert(1, 'lib')
sys.path.insert(1, 'scripts')
import road_runner
import XSS_scanner
from urllib.parse import urlparse
import tldextract


digit = 0
url = ''
dom = ''
try:  
    print("USAGE: https://domain.com/path")
    url = sys.argv[1].__str__().rstrip('\n')
    for character in url:
        if character.isdigit():
            digit = digit + 1
    if digit <= 3:
        result = urlparse(url)
        dom = result.netloc
    elif digit >= 4:
        print("This Version Do not support IP addess yet")
    try:
        path = "scripts/output/" + dom
        try:
            f = open( path ,"r")
        except:
            road_runner.run(dom)
            f = open( path ,"r")  
        lines =f.readlines()
        for line in lines:
            line = line.__str__()
            try:
                if ".png" not in line and ".js" not in line and ".css" not in line and ".jpeg" not in line and ".jpg" not in line:
                    #print(line)
                    XSS_scanner.scan_xss(line)
            except Exception as e:
                print("Exception")
                #pass
        f.close()
 
    except KeyboardInterrupt:
        print("Canceling script...")
        sys.exit(1)
except Exception as e:
    print("USAGE: https://domain.com/path")
    print("\nERROR : " + e.__str__() + "\n") 