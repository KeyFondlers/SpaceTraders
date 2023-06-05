import requests
import json
import time
import os
baseDir = "./src/"

static_pool_size = 2
burst_pool_size = 10

static_pool_cooldown = 1
burst_pool_cooldown = 10

#Request Pools
requestPool = []

#Pull the token
with open(os.path.join(baseDir, "data/TOKEN")) as file:
    token = file.read()

header = {
    "Authorization": "Bearer " + token
}

def makeAPICall(requestFile):
    
    global baseDir

    timeCard = {}

    fileDir = os.path.join(baseDir, "util/APIRequestManager/requests/", requestFile)

    startTime = time.time()
    requestJson = {}
    with open(fileDir) as json_file:
        requestJson = json.load(json_file)
    endTime = time.time()
    timeCard['requestFileLoadTime'] = endTime - startTime

    #Make the request
    startTime = time.time()
    output = requests.get(requestJson['data']['url'], headers=header)

    while "error" in output.json():
        #Save the error
        with open("error.log", 'a') as outfile:
            json.dump(output.json(), outfile, indent=4)

        time.sleep(output.json()['error']['data']['retryAfter'])
        output = requests.get(requestJson['data']['url'], headers=header)

    endTime = time.time()
    timeCard['apiRequestTime'] = endTime - startTime
    timeCard['apiCallTimestamp'] = time.time()

    #Write the output to the file
    startTime = time.time()
    with open(requestJson['data']['outputFile'], 'w') as outfile:
        json.dump(output.json(), outfile, indent=4)
    endTime = time.time()
    timeCard['outputWriteTime'] = endTime - startTime

    #Delete the request file
    startTime = time.time()
    os.remove(fileDir)
    endTime = time.time()
    timeCard['requestFileDeleteTime'] = endTime - startTime

    #Total time
    timeCard['totalTime'] = timeCard['requestFileLoadTime'] + timeCard['apiRequestTime'] + timeCard['outputWriteTime'] + timeCard['requestFileDeleteTime']

    #Get the time of the request
    timeCard['requestTime'] = time.time()

    return timeCard


class Pool:
    def __init__(self, size, cooldown):
        self.size = size
        self.cooldown = cooldown
        self.pool = []
        self.emptying = False
        self.lastInit = -1
        self.sentRequests = 0
        self.currentTask = "Init"
        self.requestTimeCard = {}
    
    def addRequest(self, request):
        self.currentTask = "Add Request"
        if len(self.pool) < self.size:
            self.pool.append(request)
            return True
        else:
            return False
    
    def removeRequest(self, request):
        self.currentTask = "Remove Request"
        if request in self.pool:
            self.pool.remove(request)

    def managePool(self):
        self.currentTask = "Manage Pool"
        if self.pool != []:
            if not self.emptying:
                self.currentTask = "First Call"
                self.emptying = True
                self.sentRequests = 0
                self.requestTimeCard = makeAPICall(self.pool[0])
                print("Made Call:", self.pool[0][:-5], "in", str(self.requestTimeCard['apiRequestTime'])[:4], "seconds")
                self.pool.pop(0)
                self.sentRequests += 1
                self.lastInit = self.requestTimeCard['apiCallTimestamp']
            if time.time() - self.lastInit < self.cooldown:
                if self.sentRequests < self.size:
                    self.currentTask = "Filling Buffer"
                    if self.pool != []:
                        makeAPICall(self.pool[0])
                        self.pool.pop(0)
                        self.sentRequests += 1
                else:
                    self.currentTask = "Waiting for Cooldown"
            if time.time() - self.lastInit >= self.cooldown:
                self.currentTask = "Resetting"
                self.emptying = False
                self.lastInit = -1
                self.sentRequests = 0
        else:
            self.currentTask = "Awaiting Requests"

    def getPool(self):
        self.currentTask = "Get Pool"
        return self.pool
    
    def getInfo(self):
        info = {}
        info['pool'] = self.pool
        info['emptying'] = self.emptying
        info['sentRequests'] = self.sentRequests
        info['currentTask'] = self.currentTask
        if(self.requestTimeCard != {}):
            info['lastRequestTime'] = self.requestTimeCard['apiRequestTime']
        info['timeSinceLastInit'] = time.time() - self.lastInit
        return info
    
static = Pool(static_pool_size, static_pool_cooldown)
burst = Pool(burst_pool_size, burst_pool_cooldown)

def fillRequestPool():
    global baseDir

    #Timecard
    timeCard = {}
    
    global requestPool
    #Get the files in the requests folder
    start = time.time()
    requestPool = os.listdir(os.path.join(baseDir,"util/APIRequestManager/requests"))
    end = time.time()

    #Remove the files that are in the pools
    for file in static.getPool():
        requestPool.remove(file)
    for file in burst.getPool():
        requestPool.remove(file)

    #Log the time it took to get to fill the pool
    timeCard['totalTime'] = end - start

    return timeCard

while True:
    timeCards = []
    timeCards.append(fillRequestPool())

    #Add requests to the pools
    while True:
        #Shift requests from the burst pool to the static pool
        while (burst.getPool() != [] and len(static.getPool()) < static_pool_size):
            static.addRequest(burst.getPool()[0])
            burst.removeRequest(burst.getPool()[0])
                    
        #Fill the pools from the request pool
        if requestPool != []:
            if not static.addRequest(requestPool[0]):
                if not burst.addRequest(requestPool[0]):
                    break
                else:
                    requestPool.pop(0)
            else:
                requestPool.pop(0)

        if requestPool == []:
            break
            
    #Manage the pools
    static.managePool()
    burst.managePool()

    #Display the pool info

    #Output pool info to file
    with open(os.path.join(baseDir, "util/APIRequestManager/PoolInfo.json"), 'w') as outfile:
        json.dump({"static": static.getInfo(), "burst": burst.getInfo()}, outfile, indent=4)




