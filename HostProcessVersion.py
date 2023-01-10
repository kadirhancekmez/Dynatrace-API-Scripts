from asyncore import read
from json import load
#from openpyxl import Workbook,load_workbook
import json
#import openpyxl
from pathlib import Path
import requests
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xlsxwriter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


#Environment
ProdEnv =

#Api-Token
ProdToken





def RestartRequiredHost(Env,Token):
    URL = "" + Env + "/api/"
    #Hostların çekilmesi
    
    
    headers = {
    'accept': 'application/json; charset=utf-8',
    'Authorization': Token,
}

    params = {
    'showMonitoringCandidates': 'false',
    'includeDetails': 'true',
    'from': 'now-2h',
    'pageSize': '4000',
}
    HostURL = URL + "v1/entity/infrastructure/hosts"
    response = requests.get(HostURL, params=params, headers=headers,verify=False)
    host = json.loads(response.text)
    
    displayName = []
    agentVersion = []
    ProcessName = []
    ProcessVersion = []
    i= 0
    true = True
    false = False
    
    for entities in host:
        #print(len(entities))
        #print(entities)
        if ("monitoringMode") in entities :
            if entities["monitoringMode"]== "FULL_STACK":
                
                if  ("isProcessOf") in entities["toRelationships"]:
                    for ProcessId in entities["toRelationships"]["isProcessOf"] : 
                        #print(entities["displayName"])
                        #print(ProcessId)
                    
                        headers = {
                            'accept': 'application/json; charset=utf-8',
                            'Authorization': Token,
                        }

                        ProcesUrl = URL + "v1/entity/infrastructure/processes/"
                        responseProcess = requests.get(ProcesUrl  +  ProcessId, headers=headers,verify=False)
                        Processs = json.loads(responseProcess.text)
                                    
                    
                        #print(Processs["monitoringState"]["restartRequired"] )
                        if ("monitoringState") in Processs:
                            #print(Processs["monitoringState"]["restartRequired"])
                            if Processs["monitoringState"]["restartRequired"] == true and ("agentVersions" in Processs) :
                                displayName.append(entities["displayName"])
                                #print(entities["displayName"])
                                if ("agentVersion" in entities):   
                                    version = str(entities["agentVersion"]["major"]) + "."+  str(entities["agentVersion"]["minor"])+ "."+ str(entities["agentVersion"]["revision"])
                                    agentVersion.append(version)
                                    #print(version)
                                
                                if ("agentVersions" in Processs):
                                    versionn = str(Processs["agentVersions"][0]["major"]) + "."+  str(Processs["agentVersions"][0]["minor"])+ "."+ str(Processs["agentVersions"][0]["revision"])
                                    ProcessVersion.append(versionn)
                                ProcessName.append(Processs["displayName"])
                                             
                i = i+1
                print(i)
        #Bunları excel formatında yazdırmak için worksheet kullanma
        workbook = xlsxwriter.Workbook('HostMonitoringRestartProddDd.xlsx')
        worksheet = workbook.add_worksheet()
        Baslık = ["Host Name","Host Version","Process Name","Process Version"]

        worksheet.write_row(0, 0, Baslık)
        worksheet.write_column(1, 0, displayName)
        worksheet.write_column(1, 1, agentVersion)
        worksheet.write_column(1, 2, ProcessName)
        worksheet.write_column(1, 3, ProcessVersion)
        workbook.close()   
        
RestartRequiredHost(ProdEnv,ProdToken)
