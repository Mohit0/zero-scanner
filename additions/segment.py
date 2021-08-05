#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import paramiko
import getpass
import os
from scp import SCPClient

print("Starting Scan: ")
hosts = ["10.86.72.24","10.87.200.86","10.87.204.23","10.112.50.5"]

username = input("\nPlease provide your SSH UserName: ")
passkey = getpass.getpass("Please provide your SSH  Password: ")
file = input("Please provide path of subnet list file: ")

for host in hosts:
        print("\nTrying to Connect with " + str(host))
        port = 22
        try:
                # connecting to SSH Host
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port, username, passkey)
                print("Host Connected.\n\nInitiating Segmentation Scan.")

                # uploading subnet list to server
                print("\nUpoading Subnet list file to server")
                sftp = ssh.open_sftp()
                sftp.put(file, '/segscan/hosts.txt')
                sftp.close()
                print("File Uploaded Succesfully. \n\nInitiating Scan using Nmap...")

                # Running nmap scan and printing output on screen
                cmd = 'sudo nmap -sS -sU --open -oX /segscan/output.xml -iL /segscan/hosts.txt'
                stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
                stdin.write(str(passkey) + "\n")
                stdin.flush()
                out = stdout.readlines()
                output = ' '.join([str(elem) for elem in out])
                print(output)

                # downloading files back to host
                sftp = ssh.open_sftp()
                sftp.get('/segscan/output.xml', str(host) + 'CTC-PCI.xml')
                sftp.close()

                # closing the SSH connection
                ssh.close()

        except Exception as e:
                print("Error Occured: " + str(e))