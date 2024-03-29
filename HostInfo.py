from asyncore import read
from json import load
from openpyxl import Workbook,load_workbook
import json
import openpyxl
from pathlib import Path
import requests
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xlsxwriter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)




#Environment
ProdEnv = ""
TestEnv = ""

#Api-Token
ProdToken = "Api-Token "
TestToken = "Api-Token "

def HostMonitor(Env,Token):
    URL = "https://gbmonitor/e/" + Env + "/api/"
    #Hostların çekilmesi
    HostURL = URL + "v2/entities?pageSize=3000&entitySelector=type%28%22HOST%22%29%2CisMonitoringCandidate%28FALSE%29&fields=properties.monitoringMode%2Cproperties.osType"
    response = requests.get(HostURL, headers={'Authorization': Token} , verify=False)
    host = json.loads(response.text)
    
    displayName = []
    monitoringMod = []
    osType = []
    
    
    for entities in host["entities"]:
        #print(len(entities["properties"]))
        displayName.append(entities["displayName"])
        if len(entities["properties"]) == 1:
            monitoringMod.append(" ")
        else:
            monitoringMod.append(entities["properties"]["monitoringMode"])
        osType.append(entities["properties"]["osType"])
        
    
    #Bunları excel formatında yazdırmak için worksheet kullanma
    workbook = xlsxwriter.Workbook('HostMonitoring.xlsx')
    worksheet = workbook.add_worksheet()
    Baslık = ["Host Name","osType","Monitoring Mode"]

    worksheet.write_row(0, 0, Baslık)
    worksheet.write_column(1, 0, displayName)
    worksheet.write_column(1, 1, osType)
    worksheet.write_column(1, 2, monitoringMod)

    


    workbook.close()   
        
        
        
        
HostMonitor(ProdEnv,ProdToken)
