import os
import requests
import json

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
    response = requests.get('https://api.spacetraders.io/v2/systems/' + str(systemID) + "/waypoints", headers=headers)

    return response;

#Write system data to file
def writeSystemData(systemID):
    data = getSystemData(systemID)
    with open(os.path.join(dataPath,"RawSystemData/System") + str(systemID) + ".json" , 'w') as file:
        json.dump(data.json(), file, indent=4)

writeSystemData("X1-NN19")