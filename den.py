from asyncore import read
from json import load
#from openpyxl import Workbook,load_workbook
import json
#import openpyxl
from pathlib import Path
from pickle import TRUE
import requests
import urllib3
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xlsxwriter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)





headers = {
    'accept': 'application/json',
    'Authorization': '',
}

Url = ""

responseuser = requests.get("", headers=headers,verify=False)
UserInfo = json.loads(responseuser.text)

User = []
UserGroup = []
Tarih = []
GirisSayi = []
gruplar = ""

for user in UserInfo:
    #print(user["id"])
    for grup in user["groups"]:
        #print(grup)
        x=0
        gruplar = gruplar+ "," +grup 
    #print(user["groups"])
    
    headers = {
        'accept': 'application/json; charset=utf-8',
        'Authorization': '',
    }

    params = {
        'pageSize': '5000',
        'filter': 'eventType("LOGIN")',
        'from': 'now-30d',
        'sort': '-timestamp',
    }

    responseLog = requests.get(
        '',
        params=params,
        headers=headers,
        verify=False
    )
    true =True
    Log = json.loads(responseLog.text)
    #print(Log)
    for ıd in Log["auditLogs"]:
        #print(ıd["user"])
        #sayac=0
        
        
        if user["id"] == ıd["user"] and ıd["success"]==true: 
            
            """if user in User:
                #index = User.index(user)
               
                sayac= sayac+1
            else:"""
            print(ıd["timestamp"])
            timestamp = ıd["timestamp"]
            #date_time = datetime.fromtimestamp(timestamp)
            Tarih.append(timestamp)
            User.append(ıd["user"])
            UserGroup.append(gruplar)
                #sayac=sayac+1
        else:
            Tarih.append(" ")
            User.append(user["id"])
            UserGroup.append(gruplar)
            print("q")
        
        #GirisSayi.append(sayac)
            
        #Bunları excel formatında yazdırmak için worksheet kullanma
        workbook = xlsxwriter.Workbook('UserControl.xlsx')
        worksheet = workbook.add_worksheet()
        Baslık = ["User","User Group","Tarih","Giriş Sayısı"]

        worksheet.write_row(0, 0, Baslık)
        worksheet.write_column(1, 0, User)
        worksheet.write_column(1, 1, UserGroup)
        worksheet.write_column(1, 2, Tarih)
        worksheet.write_column(1, 3, GirisSayi)
        workbook.close()   
        
