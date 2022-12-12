from email import header
from sqlite3 import DatabaseError
from tkinter import W
from nbformat import write
from openpyxl import Workbook
import requests
import json
import csv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xlsxwriter
import requests


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def OnegentOldVersion(Env,Token):
    
    
    Displayname = []
    MonıtoringMode = []
    osType = []
    agentVersion = []
    updateStatus = []

    headers = {
    'accept': 'application/json; charset=utf-8',
    'Authorization': Token,
}

    params = {
    'includeDetails': 'false',
    'availabilityState': 'MONITORED'
    
}
    response = requests.get(
    "https://gbmonitor/e/"  + Env +  "/api/v1/oneagents",
    params=params,
    headers=headers,
    verify=False
)
    Versıon  = json.loads(response.text)  
    
    paramsNext = {
    'includeDetails': 'false',
    'availabilityState': 'MONITORED',
    'nextPageKey': Versıon["nextPageKey"],
}
    next_page_data = requests.get(
    "https://gbmonitor/e/"  + Env +  "/api/v1/oneagents",
    params=paramsNext,
    headers=headers,
    verify=False
)
    NextData = json.loads(next_page_data.text)  
    
    for entities in (Versıon["hosts"]):
        #if entities["updateStatus"] != "UP2DATE"  #If you only want to get UP2DATE ones
        Displayname.append(entities["hostInfo"]["displayName"])
        if ("monitoringMode") in entities["hostInfo"]:
            MonıtoringMode.append(entities["hostInfo"]["monitoringMode"])
        else:
            MonıtoringMode.append("  ")
        if ("agentVersion") in entities["hostInfo"]:
            version = str(entities["hostInfo"]["agentVersion"]["major"]) + "." + str(entities["hostInfo"]["agentVersion"]["minor"]) + "." + str(entities["hostInfo"]["agentVersion"]["revision"])
            agentVersion.append(version)
        else:
            agentVersion.append("  ")
        if ("osType") in entities["hostInfo"]:
            osType.append(entities["hostInfo"]["osType"])
        else:
            osType.append("  ")
        if ("updateStatus") in entities:
            updateStatus.append(entities["updateStatus"])
        else:
            updateStatus.append("  ")
    
    nextkey = Versıon["nextPageKey"]
    print(nextkey)
    while True :
        
        print("deneme")
        
        paramsNext = {
    'includeDetails': 'false',
    'availabilityState': 'MONITORED',
    'nextPageKey': nextkey,
}
        next_page_data = requests.get(
    "https://gbmonitor/e/"  + Env +  "/api/v1/oneagents",
    params=paramsNext,
    headers=headers,
    verify=False
)
        NextData = json.loads(next_page_data.text)
        nextkey = NextData["nextPageKey"] 
        print(NextData["nextPageKey"])
        
        
        for entities in (NextData["hosts"]):
            #if entities["updateStatus"] != "UP2DATE"  #If you only want to get UP2DATE ones
 
            Displayname.append(entities["hostInfo"]["displayName"])
            if ("monitoringMode") in entities["hostInfo"]:
                MonıtoringMode.append(entities["hostInfo"]["monitoringMode"])
            else:
                MonıtoringMode.append("  ")
            if ("agentVersion") in entities["hostInfo"]:
                version = str(entities["hostInfo"]["agentVersion"]["major"]) + "." + str(entities["hostInfo"]["agentVersion"]["minor"]) + "." + str(entities["hostInfo"]["agentVersion"]["revision"])
                agentVersion.append(version)
            else:
                agentVersion.append("  ")
            if ("osType") in entities["hostInfo"]:
                osType.append(entities["hostInfo"]["osType"])
            else:
                osType.append("  ")
            if ("updateStatus") in entities:
                updateStatus.append(entities["updateStatus"])
            else:
                updateStatus.append("  ")
                
        if NextData["nextPageKey"] == None:
            break
        
    
        
        
    workbook = xlsxwriter.Workbook('UpdateHostdeneme.xlsx')
    worksheet = workbook.add_worksheet()
    Baslık = ["Host Name","osType","MonıtoringMode","AgentVersion","UpdateStatus"]

    worksheet.write_row(0, 0, Baslık)
    worksheet.write_column(1, 0, Displayname)
    worksheet.write_column(1, 1, osType)
    worksheet.write_column(1, 2, MonıtoringMode)
    worksheet.write_column(1, 3, agentVersion)
    worksheet.write_column(1, 4, updateStatus)
        
    
    
    
    
OnegentOldVersion(ProdEnv,ProdToken)
