import eel
from random import randint
import subprocess

eel.init("./src/applets/dash/web")  
  
# Exposing the random_python function to javascript
@eel.expose    
def openMap():
    subprocess.run(['python', './src/applets/map/map.py', "0", "0"])
    return "Map opened"
  
# Start the index.html file
eel.start("index.html", size=(960, 480))