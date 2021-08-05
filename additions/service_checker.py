#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from termcolor import colored
import os


def fun(dom,port):
    cmd = "nmap -sC -sV -A -Pn -vv -p " + str(port) + " " + str(dom)
    try:
        res = os.popen(cmd)
        output = res.read()
        print(output)
        f.write(output.__str__() + "\n\n")
    except Exception as e:
        print(e)
        f.write(str(e) + "\n\n")



#   MAIN FUNCTION
if __name__ == '__main__':
    try:
        print("\n DCE SERVICE CHECK USING NMAP")
        path = input("\nPlease provide the path to file: ")
        file = open(path.__str__().rstrip('\n'), "r")
        print("\n")
        f = open( "dce_test" ,"a+")
        for target in file:
            url = target.__str__().rstrip('\n').rstrip(' ')
            dom,port = url.split(":")
            print(colored("Scanning " + str(dom) + ":" + str(port) , "blue"))
            print()
            fun(dom,port)

    except KeyboardInterrupt:
        print("Canceling script...")
    except Exception as e:
        print(e)
