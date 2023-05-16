import requests
import json
import time

import data.TOKEN as TOKEN
token = TOKEN.token

#load the map
mapJson = ""
with open('data/MAP.json') as json_file:
    mapJson = json.load(json_file)

def pullJson(data, filename):
    with open("data/" + filename + '.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

def getData(key):
    headers = {
        'Authorization': ('Bearer ' + token),
    }
    response = requests.get('https://api.spacetraders.io/v2/' + key, headers=headers)

    return response;

def getAgent():
    return getData("my/agent");

def getContracts():
    return getData("my/contracts");

def getSystems():
    return getData("systems?limit=20&page=249")

def findObject(symbol):
    #Split the symbol into the sector system and object using the - deliminator
    splitSymbol = symbol.split("-")

    #Assign the split values to variables
    sector = splitSymbol[0]
    system = splitSymbol[1]
    object = splitSymbol[2]

    #Find the system in the map
    for i in range(0, len(mapJson)):
        if mapJson[i]['symbol'] == (sector + "-" + system):
            print("Found system " + system + " at system index:" + str(i))
            #Find the object in the system
            for j in range(0, len(mapJson[i]['waypoints'])):
                if mapJson[i]['waypoints'][j]['symbol'] == (sector + "-" + system + "-" + object):
                    print("Found object " + object + " at object index:" + str(j))
                    return mapJson[i]['waypoints'][j]
