import os
import requests
import json
import numpy as np
import time

dataPath = "./src/data/"

#Read token from file
tokenPath = os.path.join(dataPath, "TOKEN")
token = ""
with open(tokenPath, 'r') as file:
    token = file.read()

def getSystemData(systemID):
    headers = {
        'Authorization': ('Bearer ' + token),
    }

    data = []

    #Get the first page of data
    response = requests.get('https://api.spacetraders.io/v2/systems/' + str(systemID) + "/waypoints", headers=headers)
    data.append(response.json()["data"])
    time.sleep(0.51);
    
    #Get the total data count
    dataCount = response.json()["meta"]["total"]
    limit = response.json()["meta"]["limit"]

    #Count the number of pages
    pages = int(np.ceil(dataCount / limit))

    #Get the data from the remaining pages
    for i in range(2, pages + 1):
        response = requests.get('https://api.spacetraders.io/v2/systems/' + str(systemID) + "/waypoints?page=" + str(i), headers=headers)
        data.append(response.json()["data"])
        time.sleep(0.51);

    return data;

#Write system data to file
def writeSystemData(systemID):
    data = getSystemData(systemID)
    with open(os.path.join(dataPath,"Map/RawSystemData/") + str(systemID) + ".json" , 'w') as file:
        json.dump(data, file, indent=4)


writeSystemData("X1-TZ19");