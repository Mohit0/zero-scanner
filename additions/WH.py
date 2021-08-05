#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

# BELOW FUNCTION CREATES STORY FOR RALLY

def rally_fun(asset):
    print("Creating Rally Story For: " + asset)
    url_rally = "https://rally1.rallydev.com/slm/webservice/v2.x/hierarchicalrequirement/create"
    true = "true"
    false = "false"

    headerss = {
    "User-Agent": "Mozilla/5.0 X11; Linux x86_64; rv:68.0 Gecko/20100101 Firefox/68.0", 
    "Cookie": "ZSESSIONID=_mpZhGTxlQWOxLzGpKG0PdLgZ2WWkfNtIteml71Emo", 
    "Connection": "close", 
    "Upgrade-Insecure-Requests": "1",
    "accept": "application/json",
    }

    data = {"HierarchicalRequirement":{"Name": "WH Zero Scan on " + asset,"Project":{"OID":256426520944,"Name":"EIS TVM Ethical Hacking","_refObjectUUID":"ca633b80-bf1f-472c-8252-ace07e3f2bd1","State":"Open","_p":"0","_ref":"/project/256426520944","Workspace":{"WorkspaceConfiguration":{"DateFormat":"yyyy-MM-dd","WorkDays":"Monday,Tuesday,Wednesday,Thursday,Friday","_refObjectUUID":"6ac52ea1-b49e-4e58-9f43-105e8391ca4d","DragDropRankingEnabled":true,"_p":"0","DateTimeFormat":"yyyy-MM-dd","IterationEstimateUnitName":"Points","TaskUnitName":"Hours","_ref":"/workspaceconfiguration/14457458599","TimeTrackerEnabled":false,"BuildandChangesetEnabled":true,"_type":"WorkspaceConfiguration","TimeZone":"America/Chicago","ObjectID":14457458599,"ReleaseEstimateUnitName":"Points"},"OID":14457696030,"Name":"UHG","_refObjectUUID":"1d47ac97-ec8d-4bd7-97a3-31bcfba9a03d","State":"Open","_p":"0","_ref":"/workspace/14457696030","SchemaVersion":"770e3cf7e429e4bf040440371ca933b5","_type":"Workspace","ObjectID":14457696030,"_refObjectName":"UHG","Children":{"_ref":"/Workspace/14457696030/Children","_type":"Project","Count":0}},"SchemaVersion":"4b5adeb0929018da138b51860d759d09","ObjectID":256426520944,"_refObjectName":"EIS TVM Ethical Hacking","Children":{"_ref":"/Project/256426520944/Children","_type":"Project","Count":0}},"Owner":{"LandingPage":"/dashboard","LastSystemTimeZoneName":"Asia/Calcutta","DashboardRole":"CONTRIBUTOR","DisplayName":"Mohit Verma","CreationDate":"2019-05-15T22:30:32.000Z","_refObjectUUID":"d10ab2c3-81c8-4d52-82c4-f8d531876f72","Planner":false,"_ref":"/user/307746165988","Role":"Development Team","UserName":"mohit.verma@optum.com","Version":437,"ObjectID":307746165988,"FirstName":"Mohit","InvestmentAdmin":false,"CanCreateUsers":false,"_refObjectName":"Mohit Verma","UserProfile":{"DefaultDetailPageToViewingMode":false,"DateFormat":"","DateTimeFormat":"","VersionId":"3","_ref":"/userprofile/307746165996","Language":"en-US","TimeZone":"America/Chicago","ObjectID":307746165996,"Locale":"en-US","EmailNotificationEnabled":true,"WelcomePageHidden":false}}}}


    try:
        response = requests.post(url_rally, headers=headerss, json=data)
        print("Story Created Successfully.\n")
    except Exception as e:
        print("Exception Occured: " + str(e))

    #parsed = json.loads(response.text)
    #print(json.dumps(parsed, indent=4))
    



# BELOW CODE FETCHES DATA FROM WHITEHAT AND SENDS DATA TO RALLY_FUN() FUNCTION

url = "https://source.whitehatsec.com/api/v2/assets"

querystring = {"fields":"actionItems","minActionItemsCount":"1","limit":"10","offset":"0","sort":"name","actionType":"has_access_issues"}
 

headers = {
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0", 
"Key": "e46cc658-2183-423a-8540-6de442eb9dbe", 
"Connection": "close", 
"Upgrade-Insecure-Requests": "1",
"accept": "application/json",
}

try: 
    response = requests.get(url, headers=headers, params=querystring)
except Exception as e:
    print("Exception Occured: " + str(e))
    exit(1)

parsed = json.loads(response.text)
counted = json.dumps(parsed['page']['filteredCount'], indent=4)
if counted == 0:
    print("No Application Found")
else: 
    print("Count of Applications: " + str(counted) + "\n")
    for count in range(int(counted)):
        asset = json.dumps(parsed['collection'][count]['name'], indent=4)
        rally_fun(asset.replace('"', ''))
        break

print("THANKS YOU FOR USING THE SCRIPT\n")





