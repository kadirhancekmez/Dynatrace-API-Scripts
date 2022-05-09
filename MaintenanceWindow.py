from tkinter import W
from nbformat import write
from openpyxl import Workbook
import requests
import json
import csv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xlsxwriter

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


#Environment
ProdEnv = "---------"
TestEnv = "---------"

#Api-Token
ProdToken = "Api-Token .............."
TestToken = "Api-Token .............."

#Function that gives list of scheduled hosts from OneAgent Update
def ScheduleListHost(env,Token):
    URL = "https://gbmonitor/e/" + env + "/api/"
    #Pulling hosts with API
    HostURL = URL + "v2/entities?pageSize=400&entitySelector=type%28%22HOST%22%29"
    response = requests.get(HostURL, headers={'Authorization': Token} , verify=False)
    host = json.loads(response.text)
    
    #After the control in the loop, I created a list to add the desired hosts.
    HostList = []
    ScheduleName = []


    for entities in host["entities"]:
        #print(entities["entityId"])
        
        #Getting the OA-AutoUpdate information of the pulled hosts
        OAHostUrl = URL + "config/v1/hosts/" + entities["entityId"]   + "/autoupdate"
        responseOA = requests.get(OAHostUrl, headers={'Authorization': Token} , verify=False)
        OA = json.loads(responseOA.text)

        #Extracting OA-AutoUpdate information
        for entity in OA["updateWindows"]["windows"]:
            #print(entities["name"])
            
            #Adding the names of valid hosts to the list
            HostList.append(entities["displayName"])
            #List the Schedule Name corresponding to the hosts
            ScheduleName.append(entity["name"])
            #Converting to dict format to read 2 lists properly
            Result = dict(zip(HostList,ScheduleName))

    #control
    print(Result)
            
    #Using worksheet to print them in excel format
    workbook = xlsxwriter.Workbook('ScheduleListHost.xlsx')
    worksheet = workbook.add_worksheet()
    
    col_num = 1

    for key, value in Result.items():
        worksheet.write(0,0,"Host Name")
        worksheet.write(0,1,"Schedule Name")
        worksheet.write(col_num,0,key)
        worksheet.write(col_num,1,value)
        col_num += 1


    workbook.close()   
    

#You can access it by entering the environment you want and its Api-Token.
ScheduleListHost(ProdEnv,ProdToken)
#ScheduleListHost(TestEnv,TestToken)
