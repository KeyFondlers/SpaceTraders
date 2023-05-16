import os
import requests
import time
import json
from tqdm import tqdm

dataPath = "./src/data/"

#Read token from file
tokenPath = os.path.join(dataPath, "TOKEN")
token = ""
with open(tokenPath, 'r') as file:
    token = file.read()

TOTAL_SYSTEMS = 7000;
PAGE_LIMIT = 20;
RATE_LIMIT = 0.55; #Delay after request

def getMapPage(pageNum):
    headers = {
        'Authorization': ('Bearer ' + token),
    }
    response = requests.get('https://api.spacetraders.io/v2/systems?limit=20&page=' + str(pageNum), headers=headers)

    return response;

def pullMapData():
    for i in tqdm(range(1,int(TOTAL_SYSTEMS/PAGE_LIMIT) + 1)):
        page = getMapPage(i)
        with open(os.path.join(dataPath,"RawMapData/Page") + str(i) + ".json" , 'w') as file:
            json.dump(page.json(), file, indent=4)
        time.sleep(RATE_LIMIT)

def mergeMapData():
    data = []
    for i in tqdm(range(1,int(TOTAL_SYSTEMS/PAGE_LIMIT) + 1)):
        with open(os.path.join(dataPath,"RawMapData/Page") + str(i) + ".json") as json_file:
            jsonData = json.load(json_file)
            for i in range(0, len(jsonData['data'])):
                data.append(jsonData['data'][i])

    with open(os.path.join(dataPath,"Map.json"), 'w') as outfile:
        json.dump(data, outfile, indent=4)

#pullMapData();
mergeMapData();