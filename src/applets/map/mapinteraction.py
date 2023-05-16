import subprocess
import os

testCoordinate = (0, 0)
testSystem = "X1-BD56"

print(os.listdir("./src/applets/map"))

subprocess.run(['python', './src/applets/map/map.py', str(testCoordinate[0]), str(testCoordinate[1])])

#subprocess.run(['python', 'map.py', testSystem])

