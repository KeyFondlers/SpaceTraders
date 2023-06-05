import os
import json
import numpy as np
import time
import datetime

import sys
sys.path.append("./src/util/APIRequestManager/")
import Interface as api
from Interface import APIRequest

baseURL = "https://api.spacetraders.io/v2/systems"
tmpDir = "./src/util/MapGenerator/tmp"

LIMIT = 20
TOTAL_SYSTEMS = 1
PAGE_COUNT = 1

def getGalaxyData():
    #Request a bit of data to get the total number of systems
    apiRequest = api.sendRequest(
        APIRequest(
            url = baseURL + "?limit=1&page=1",
            outputFile = tmpDir + "/tmp.json",
            priority = 0,
            src = "MapGenerator"
        )
    )
    #Wait until tmp.json is created
    while not os.path.exists(tmpDir +"/tmp.json"):
        pass
    time.sleep(0.01)

    #Read the data from tmp.json
    with open(tmpDir + "/tmp.json") as json_file:
        global TOTAL_SYSTEMS
        global PAGE_COUNT
        jsonData = json.load(json_file)
        TOTAL_SYSTEMS = jsonData['meta']['total']
        PAGE_COUNT = int(np.ceil(TOTAL_SYSTEMS / LIMIT))
    
    #Delete tmp.json
    os.remove(tmpDir + "/tmp.json")

def requestAllMapData():
    for i in range(1,PAGE_COUNT + 1):
        apiRequest = api.sendRequest(
            APIRequest(
                baseURL + f"?limit={LIMIT}&page={i}",
                tmpDir + f"/MapPage{i}.json",
                0,
                "MapGenerator"
            )
        )


def mergeMapData():
    data = []
    for i in range(1,PAGE_COUNT + 1):
        with open(tmpDir + f"/MapPage{i}.json") as json_file:
            jsonData = json.load(json_file)
            for i in range(0, len(jsonData['data'])):
                data.append(jsonData['data'][i])

    with open("./src/data/Map/Map.json", 'w') as outfile:
        json.dump(data, outfile, indent=4)

    #Delete all the pages
    for i in range(1,PAGE_COUNT + 1):
        os.remove(tmpDir + f"/MapPage{i}.json")

#Get the total number of systems and pages
getGalaxyData()

print("Galaxy Data Received")
print(f"Total Systems: {TOTAL_SYSTEMS}")
print(f"Total Pages: {PAGE_COUNT}")

#Request all the data
requestAllMapData()

start = time.time()

print("Waiting for all requests to complete...")

#Wait until all the requests are completed
while(len(os.listdir(tmpDir)) != PAGE_COUNT):
    pass
end = time.time()

print("All requests completed")

#Map Generation Time
print(f"Map Generation Time: {end - start}")

#Average time per request
print(f"Average time per request: {(end - start) / PAGE_COUNT}")

#Average Requests per second
print(f"Requests Per Second: {PAGE_COUNT / (end - start)}")

print("Merging Data...")

#Merge the data
mergeMapData()

print("Data Merged")


