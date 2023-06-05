import os
import time
from consoledraw import Console
console = Console()

baseDir = "./src/"
while True:
    with open(os.path.join(baseDir, "util/APIRequestManager/poolInfo.json"), 'r') as info:
        with console:
            console.print(info.read())
    time.sleep(0.1)