import os
import requests
import time
import json
import numpy as np
from tqdm import tqdm
import sys

dataPath = "./src/data/"

#Read token from file
tokenPath = os.path.join(dataPath, "TOKEN")
token = ""
with open(tokenPath, 'r') as file:
    token = file.read()

RATE_LIMIT = 1 / 2 # 2 requests per 1.1 seconds
NEXT_ALLOWED_REQUEST = time.time()

def getMapPage(pageNum):
    headers = {
        'Authorization': ('Bearer ' + token),
    }
    response = requests.get('https://api.spacetraders.io/v2/systems?limit=20&page=' + str(pageNum), headers=headers)

    #Check for errors
    try:
        tmp = response.json()['data']
        pass

    except:
        print("Error: " + response.json()['error']['message'])
        print("Exiting...")
        sys.exit(1)


    #Rate limit
    global NEXT_ALLOWED_REQUEST
    if (NEXT_ALLOWED_REQUEST > time.time()):
        time.sleep(NEXT_ALLOWED_REQUEST - time.time())

    NEXT_ALLOWED_REQUEST = time.time() + RATE_LIMIT

    return response;

#Get map page 1
page = getMapPage(1)

#Get the total data count
TOTAL_SYSTEMS = page.json()["meta"]["total"]
PAGE_LIMIT = page.json()["meta"]["limit"]

#Get the number of pages
PAGE_COUNT = int(np.ceil(TOTAL_SYSTEMS / PAGE_LIMIT))

def clearTempData():
    #Clear temp page files
    for i in tqdm(range(1,PAGE_COUNT + 1)):
        try:
            os.remove(os.path.join(dataPath,"Map/RawMapData/Page") + str(i) + ".json")
        except:
            pass

def pullMapData():
    for i in tqdm(range(1,PAGE_COUNT + 1)):
        page = getMapPage(i)
        with open(os.path.join(dataPath,"Map/RawMapData/Page") + str(i) + ".json" , 'w') as file:
            json.dump(page.json(), file, indent=4)

def mergeMapData():
    data = []
    for i in tqdm(range(1,PAGE_COUNT + 1)):
        with open(os.path.join(dataPath,"Map/RawMapData/Page") + str(i) + ".json") as json_file:
            jsonData = json.load(json_file)
            for i in range(0, len(jsonData['data'])):
                data.append(jsonData['data'][i])

    with open(os.path.join(dataPath,"Map/Map.json"), 'w') as outfile:
        json.dump(data, outfile, indent=4)


def regenerateMap():
    clearTempData();
    pullMapData();
    mergeMapData();
    clearTempData();

regenerateMap();
