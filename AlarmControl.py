def add_to_counter(x, ManagmentZone, counter):
    if x["impactLevel"] == "SERVICES":
        counter[ManagmentZone]["fs"] += 1
    if x["impactLevel"] == "INFRASTRUCTURE":
        counter[ManagmentZone]["io"] += 1
    if x["impactLevel"] == "PROCESS_GROUP_INSTANCE":
        counter[ManagmentZone]["io"] += 1
    if x["impactLevel"] == "APPLICATION" :
        counter[ManagmentZone]["app"] += 1
    return counter

def Alarm(GeneralUrl,ENV,Token):
    headers = {
    'accept': 'application/json; charset=utf-8',
    'Authorization': Token,
    }
    params = {
    'pageSize': '500',
    }
    responseALARM = requests.get(GeneralUrl + ENV + '/api/v2/problems', headers=headers, params=params,verify=False)
    Alarm = json.loads(responseALARM.text)

    counter = {}
    #print(Alarm["totalCount"])
    
    for x in Alarm["problems"]:
        #print(len(x["managementZones"]))
        #print(counter)
        if len(x["managementZones"]) != 0:
            if  x["managementZones"][0]["name"] not in counter: 
                #print(x["managementZones"][0]["name"])
                ManagmentZone = x["managementZones"][0]["name"]
                counter[ManagmentZone] = {"io":0 , "fs":0 , "app":0 }    
                
            counter = add_to_counter(x, ManagmentZone, counter)
            
            
        else:    
            ManagmentZone = "YOK"
            if  ManagmentZone not in counter:   
                counter[ManagmentZone] = {"io":0 , "fs":0 , "app":0 }
            counter = add_to_counter(x, ManagmentZone,counter)
            
    df = pd.DataFrame.from_dict(counter, orient='index')
    df.to_excel("counter.xlsx")

Alarm(GeneralUrl,ProdEnv,ProdToken)  
