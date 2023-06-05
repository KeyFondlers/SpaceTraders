import datetime
import os
import json

class APIRequest:
    def __init__(self, url=r"n/a", outputFile=r"n/a", priority=5, src="Non Specified"):
        self.url = url
        self.outputFile = outputFile
        self.priority = priority
        self.src = src

requestTemplate = {}

#Load Request Tempalte
with open("./src/util/APIRequestManager/RequestTemplate.json") as json_file:
    requestTemplate = json.load(json_file)

def get6DigitPriority(priority):
    priorityLength = len(str(priority))
    prefix = ""
    for i in range(0, 6 - priorityLength):
        prefix += "0"
    return prefix + str(priority)

def sendRequest(apiRequest):

    global requestTemplate
    requestData = requestTemplate

    requestData['data']['url'] = apiRequest.url
    requestData['data']['outputFile'] = apiRequest.outputFile
    requestData['data']['priority'] = apiRequest.priority
    requestData['meta']['source'] = apiRequest.src
    requestData['meta']['timestamp'] = str(datetime.datetime.now())

    #Get the number of requests with the same priority
    priorityCount = 0
    for file in os.listdir("./src/util/APIRequestManager/requests"):
        if file.startswith("Priority" + str(requestData['data']['priority']) + "-"):
            priorityCount += 1

    #Write the json file
    outputFileDir = "./src/util/APIRequestManager/requests/Priority" + str(requestData['data']['priority']) + "-" + "Request" + get6DigitPriority(priorityCount) + ".json"
    
    with open(outputFileDir, 'w') as outfile:
        json.dump(requestData, outfile, indent=4)

    #Wait for file to be fully written
    while not os.path.exists(outputFileDir):
        pass

    return "Request Received"