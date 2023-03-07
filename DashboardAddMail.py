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



GenerelURL =''
#Dashboard ID 
DashboardID = "b"

Mail = ["kadirhn.cekez","deneme2","den3"]

def DashboardReportUserMAil(env,token,dashboardıd,mail):
    headers = {
    'accept': 'application/json; charset=utf-8',
    'Authorization': token,
}

    params = {
    'type': 'DASHBOARD',
    'sourceId': dashboardıd,
}

    response = requests.get(
    GenerelURL + env + '/api/config/v1/reports',
    params=params,
    headers=headers,
    verify=False,
)
    dhıd = json.loads(response.text)
    
    raporıd = dhıd["values"][0]["id"]
    
    responserapoıd = requests.get(
    GenerelURL + env +'/api/config/v1/reports/' + raporıd,
    headers=headers,
    verify=False,
)
    raporread = json.loads(responserapoıd.text)
    #mail_json = json.dumps(mail)
    #print(raporread["subscriptions"]["WEEK"][1])
    y=0
    for x in raporread["subscriptions"]["WEEK"]:
        print(raporread["subscriptions"]["WEEK"][y])
        if raporread["subscriptions"]["WEEK"][y] not in mail:
            mail.append(raporread["subscriptions"]["WEEK"][y])
        y=y+1
    
    for i in mail:
        raporread["subscriptions"]["WEEK"]=mail
        raporread["subscriptions"]["MONTH"]=mail
    
    print(raporread)
    headers = {
    'accept': 'application/json; charset=utf-8',
    'Authorization': token,
    'Content-Type': 'application/json; charset=utf-8',
}
    responseputdh = requests.put(
    GenerelURL + env +'/api/config/v1/reports/' + raporıd,
    headers=headers,
    json=raporread,
    verify=False,
)
    
    print(responseputdh.status_code)
    
DashboardReportUserMAil(ProdEnv,ProdToken,DashboardID,Mail)
