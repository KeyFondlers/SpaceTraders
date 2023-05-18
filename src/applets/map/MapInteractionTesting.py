import subprocess
import os

testCoordinate = (13, -14)
testSystem = "X1-BD56"

subprocess.run(['python', './src/applets/map/map.py', str(testCoordinate[0]), str(testCoordinate[1])])
#subprocess.run(['python', './src/applets/map/map.py', testSystem])

