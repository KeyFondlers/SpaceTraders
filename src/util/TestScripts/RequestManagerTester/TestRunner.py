import json
import time
import os


baseUrl = "https://api.spacetraders.io/v2/my/agent"
outputDir = "./src/util/TestScripts/RequestManagerTester/output"

#Delete all the output files
for file in os.listdir(outputDir):
    os.remove(os.path.join(outputDir, file))

requestCount = 100

start = time.time()
for i in range(1, requestCount + 1):
    request = api.APIRequest()
    request.url = baseUrl
    request.priority = 0
    request.outputFile = outputDir + "/request" + str(i) + ".json"
    request.src = "testRequestGenerator.py"
    api.sendRequest(request)

print("Requested " + str(requestCount) + " requests")

#Wait for all requests to be fufilled
while len(os.listdir(outputDir)) < requestCount:
    pass

end = time.time()

#Average time per request
print("Average Request Time:", (end - start) / requestCount)

#Average Requests per second
print("Requests Per Second:", requestCount / (end - start))

#Total Time
print("Total Time:", end - start)

#Count errors
errorCount = 0
for file in os.listdir(outputDir):
    with open(os.path.join(outputDir, file)) as json_file:
        data = json.load(json_file)
        if 'error' in data:
            #Print the error
            print("Error in " + file)
            print(json.dumps(data, indent=4))
            errorCount += 1

print("Error Count: " + str(errorCount))


