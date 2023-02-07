def add_to_counter(x, ManagmentZone, counter):
    if x["impactedEntities"][0]["entityId"]["type"] == "SERVICE":
        counter[ManagmentZone]["fs"] += 1
    elif x["impactedEntities"][0]["entityId"]["type"] == "HOST":
        hostıd = (x["impactedEntities"][0]["entityId"]["id"])

        responseHost = requests.get(
        GeneralUrl + ENV + '/api/v2/entities/' + hostıd ,
        headers=headers,
        verify=False
        )
        HostInfo = json.loads(responseHost.text)
        i = HostInfo["properties"]["monitoringMode"]
        print(i)
        if i == "FULL_STACK":
                counter[ManagmentZone]["fs"] += 1
        else:      
                counter[ManagmentZone]["io"] += 1
    else:
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
    responseALARM = requests.get(GeneralUrl + ENV + '/api/v2/problems', headers=headers,verify=False)
    Alarm = json.loads(responseALARM.text)

    counter = {}
    
    for x in Alarm["problems"]:
        #print(len(x["managementZones"]))
        #print(counter)
        if len(x["managementZones"]) != 0:
            if  x["managementZones"][0]["name"] not in counter: 
                ManagmentZone = x["managementZones"][0]["name"]
                counter[ManagmentZone] = {"io":0 , "fs":0 , "app":0 }
            counter = add_to_counter(x, ManagmentZone, counter)
        else:
            ManagmentZone = "YOK"
            counter[ManagmentZone] = {"io":0 , "fs":0 , "app":0 }
            counter = add_to_counter(x, ManagmentZone, counter)
    print(counter)

Alarm(GeneralUrl,ProdEnv,ProdToken)  
