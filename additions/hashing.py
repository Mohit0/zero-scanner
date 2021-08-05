import hashlib
import os
from pyaxmlparser import APK

BLOCKSIZE = 65536       

fileToOpen = input("Enter name of file to calculate hash values: ")

hasher = hashlib.md5()
sha1 = hashlib.sha1()
sha256 = hashlib.sha256()

with open(fileToOpen, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    
    while len(buf) > 0:
        hasher.update(buf)
        sha1.update(buf)
        sha256.update(buf)
        
        buf = afile.read(BLOCKSIZE)
        
file_size = os.path.getsize(fileToOpen)
print("\nFile Name: " + str(fileToOpen))
print("File Size: " + str(file_size) + " bytes")
print("MD5: {0}".format(hasher.hexdigest()))
print("SHA1: {0}".format(sha1.hexdigest()))
print("SHA256: {0}".format(sha256.hexdigest()))
print("\nPackage Details: ")

if (".apk" in str(fileToOpen)):
    apk = APK(fileToOpen)
    print("Name: " + str(apk.application))
    print("Package Name: " + str(apk.package))
    print("Main Activity: " + str(apk.get_main_activity()))
    print("Version Name: " + str(apk.version_name))
    print("Version Code: " + str(apk.version_code))
    print("Target SDK: " + str(apk.get_target_sdk_version()))
    print("Minimum SDK: " + str(apk.get_min_sdk_version()))
    print("Maximum SDK: " + str(apk.get_max_sdk_version()))

import plistlib
import fnmatch
from zipfile import ZipFile

def parse_ipa_info(ipa_path):
    ipa_zip = ZipFile(ipa_path)
    files = ipa_zip.namelist()
    info_plist = fnmatch.filter(files, "Payload/*.app/Info.plist")[0]
    info_plist_bin = ipa_zip.read(info_plist)
    parse_plist(info_plist_bin)

def parse_plist(info_plist_string):
    p2 = plistlib.loads(info_plist_string)
    #print(p2)
    print("App Name: " + p2['CFBundleDisplayName'])
    print("Display Name: " + p2['CFBundleExecutable'])
    print("Identifier: " + p2['CFBundleIdentifier'])
    print("SDK Name: " + p2['DTPlatformName'] + p2['DTPlatformVersion'])
    print("Minimum OS Version: " + p2['MinimumOSVersion'])
if (".ipa" in str(fileToOpen)):
    parse_ipa_info(fileToOpen)