import os
import json
from PIL import Image
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

mapData = {}

#Import Map Data
with open("./src/data/Map/Map.json", "r") as read_file:
    mapData = json.load(read_file)


#Get maximum and minimum coordinates
maxX = -9999999
minX = 9999999
maxY = -9999999
minY = 9999999

for system in mapData:
    if system["x"] > maxX:
        maxX = system["x"]
    if system["x"] < minX:
        minX = system["x"]
    if system["y"] > maxY:
        maxY = system["y"]
    if system["y"] < minY:
        minY = system["y"]


#X values
x = [system["x"] for system in mapData]
x = np.array(x)

#Y values
y = [system["y"] for system in mapData]
y = np.array(y)

# disabling xticks by Setting xticks to an empty list
plt.xticks([]) 
 
# disabling yticks by setting yticks to an empty list
plt.yticks([]) 

plt.tick_params(axis='both', which='both', bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)

#Generate Heatmap
heatmap, xedges, yedges = np.histogram2d(x, y, bins=1000)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

#Plot Heatmap
plt.clf()

plt.imshow(heatmap.T, extent=extent, origin='lower')

plt.show()
# plt.savefig("./src/data/Map/MapHeatmap.png", dpi=300)