def ProcessOnSERVICE(env,TOKEN):
    URL = GeneralUrl + env + "/api/"
    #lıst
    ProcessGruopName = []
    ServıceName = []
    
    
    #Servıslerın çekilmesi
    ServıceURL = URL + "v2/entities?pageSize=4000&entitySelector=type%28%22SERVICE%22%29%2C%20serviceType%28%22CUSTOM_SERVICE%22%29&from=now-3M&fields=%2Bproperties.serviceType%2C%2BfromRelationships.runsOn"
    responseSERVICE = requests.get(ServıceURL, headers={'Authorization': TOKEN} , verify=False)
    Servıce = json.loads(responseSERVICE.text)
    
    
    for ıd in Servıce["entities"]:
        #print(ıd["fromRelationships"]["runsOn"][0]["id"])
        if ("runsOn")  in ıd["fromRelationships"]:
            ID = ıd["fromRelationships"]["runsOn"][0]["id"]
            ProcessURL = URL + "v2/entities/" + ID
            responsePROCESS = requests.get(ProcessURL, headers={'Authorization': TOKEN} , verify=False)
            ProcessName = json.loads(responsePROCESS.text)
            #print(ProcessName["displayName"])
            ServıceName.append(ıd["displayName"])
            ProcessGruopName.append(ProcessName["displayName"])
        else:
            ServıceName.append(ıd["displayName"])
            ProcessGruopName.append("  ") 
            
            
    workbook = xlsxwriter.Workbook('ProcessGroup.xlsx')
    worksheet = workbook.add_worksheet()
    Baslık = ["ServıceName","ProcessGruopName"]

    worksheet.write_row(0, 0, Baslık)
    worksheet.write_column(1, 0, ServıceName)
    worksheet.write_column(1, 1, ProcessGruopName)
    #worksheet.write_column(1, 2, monitoringMod)
        
        
    
ProcessOnSERVICE(ProdEnv,ProdToken)   
