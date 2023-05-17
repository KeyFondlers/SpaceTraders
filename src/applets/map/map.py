import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import math
import json
import sys

import util.Constants as Constants

def getTextboxSize(text, font, fontsize, padding):
    #Split text into lines
    lines = text.splitlines()

    #Font
    font = pygame.font.SysFont(font, fontsize)

    #Text Lines
    textLines = []

    for i in range(0, len(lines)):
        textSurface = font.render(lines[i], True, (0,0,0))
        textRect = textSurface.get_rect()
        textLines.append([textSurface, textRect])

    #Calculate longest surface
    longestSurface = 0
    for surface in textLines:
        if surface[1].width > longestSurface:
            longestSurface = surface[1].width
    
    #Calculate height of all surfaces
    totalHeight = 0
    for surface in textLines:
        totalHeight += surface[1].height

    #Return size of the box
    return (longestSurface + (padding * 2), totalHeight + (padding * 2))

def getTextDisplay(text, topLeftPos, font, fontsize, backgroundColor, borderColor, borderWidth, textColor, padding):

    textBoxSize = getTextboxSize(text, font, fontsize, padding)

    #See if the box is off the screen
    if topLeftPos[0] + textBoxSize[0] > width:
        topLeftPos = (width - textBoxSize[0], topLeftPos[1])
    if topLeftPos[1] + textBoxSize[1] > height:
        topLeftPos = (topLeftPos[0], height - textBoxSize[1])

    #Draw background centered on centerPos
    backgroundRect = pygame.Rect(0, 0, textBoxSize[0], textBoxSize[1])
    backgroundRect.topleft = topLeftPos
    pygame.draw.rect(screen, backgroundColor, backgroundRect, 0, border_radius=15)

    #Draw border
    borderRect = pygame.Rect(0, 0, textBoxSize[0], textBoxSize[1])
    borderRect.topleft = topLeftPos
    pygame.draw.rect(screen, borderColor, borderRect, borderWidth, border_radius=15)

    #Split text into lines
    lines = text.splitlines()

    #Font
    font = pygame.font.SysFont(font, fontsize)

    #Text Lines
    textLines = []
    for i in range(0, len(lines)):
        textSurface = font.render(lines[i], True, textColor)
        textRect = textSurface.get_rect()
        textLines.append([textSurface, textRect])

    #Draw text
    yOffset = padding
    for surface in textLines:
        surface[1].topleft = (topLeftPos[0] + padding, topLeftPos[1] + yOffset)
        screen.blit(surface[0], surface[1])
        yOffset += surface[1].height


def formatWaypoint(waypoint):
    #Replate _ with space
    waypoint = waypoint.replace("_", " ")
    #Lowercase
    waypoint = waypoint.lower()
    #Capitalize words
    waypoint = waypoint.title()

    return waypoint

mapData = {}

#Import Map Data
with open("./src/data/Map.json", "r") as read_file:
    mapData = json.load(read_file)

# Initialize Pygame
pygame.init()

#color pallete class
class color:
    def __init__(self):
        self.white = (255, 252, 242)
        self.lightgray = (204, 197, 185)
        self.darkgray = (64, 61, 57)
        self.black = (37, 36, 34)
        self.orange = (235, 94, 40)

pallette = color()

# Set up the window
width = 825
height = 615
screen = pygame.display.set_mode((width, height))

#Grid Size
gridSize = 15

pygame.display.set_caption("Universe Map")

# Set up the clock
clock = pygame.time.Clock()

#Dictionary of map tiles filled with "space"
mapTiles = {}

def setTile(x, y, data):
    mapTiles[(x, y)] = data

#Put all tiles in the map data into the mapTiles dictionary
for system in mapData:
    
    systemName = system["symbol"]
    systemX = int(system["x"])
    systemY = int(system["y"])
    systemType = system["type"]

    #Add the system to the map
    mapTiles[(systemX, systemY)] = []
    mapTiles[(systemX, systemY)].append([systemName, systemType])

    waypoints = system["waypoints"]

    for waypoint in waypoints:
        waypointX = systemX + int(waypoint["x"])
        waypointY = systemY + int(waypoint["y"])
        waypointName = waypoint["symbol"]
        waypointType = waypoint["type"]
        
        if (waypointX, waypointY) in mapTiles:
            mapTiles[(waypointX, waypointY)].append([waypointName, waypointType])
        else:
            mapTiles[(waypointX, waypointY)] = []
            mapTiles[(waypointX, waypointY)].append([waypointName, waypointType])
        


def checkIfTileIsVisible(x,y):
    if x in visibleXRange and y in visibleYRange:
        return True
    else:
        return False
    
#Convert Screen Coordinate to Tile Coordinate
def windowPosToTile(x, y, xOffset, yOffset):
    tileX = int((x) / gridSize) - int(xOffset)
    tileY = int((y) / gridSize) - int(yOffset)
    return (tileX, -tileY)

userXOffset = 0
userYOffset = 0

#Check if coordinates were passed
if(len(sys.argv) == 3):
    userXOffset = -int(sys.argv[1])
    userYOffset = int(sys.argv[2])

if(len(sys.argv) == 2):
    #Find the system in the map
    for i in range(0, len(mapData)):
        if sys.argv[1] == mapData[i]['symbol']:
            userXOffset = -int(mapData[i]['x'])
            userYOffset = int(mapData[i]['y'])
            break

# Set up the game loop
running = True
while running:

    #Offsets so 0,0 is the center of the screen at the beginning
    xOffset = ((width // gridSize) // 2) + int(userXOffset)
    yOffset = ((height // gridSize) // 2) + int(userYOffset)

    visibleXRange = range(-xOffset, (width // gridSize) - xOffset)
    visibleYRange = range(yOffset - (height // gridSize), yOffset)


    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            direction = event.y
            if direction == -1:
                if gridSize > 1:
                    gridSize -= 1
            elif direction == 1:
                gridSize += 1
        
        #Add mouse drag distance to the offset
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseStartX, mouseStartY = pygame.mouse.get_pos()
            if event.button == 3:
                mouseStartX, mouseStartY = pygame.mouse.get_pos()
            
        #Add mouse drag distance to the offset as long as the mouse button is held down
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:
                mouseEndX, mouseEndY = pygame.mouse.get_pos()
                userXOffset += (mouseEndX - mouseStartX) / gridSize
                userYOffset += (mouseEndY - mouseStartY) / gridSize
                mouseStartX, mouseStartY = pygame.mouse.get_pos()
            if event.buttons[2] == 1:
                mouseEndX, mouseEndY = pygame.mouse.get_pos()
                userXOffset += (mouseEndX - mouseStartX) / gridSize
                userYOffset += (mouseEndY - mouseStartY) / gridSize
                mouseStartX, mouseStartY = pygame.mouse.get_pos()
            

    # Draw to the screen
    screen.fill(pallette.black)
    
    # Draw the grid
    for x in range(0, width, gridSize):
        pygame.draw.line(screen, pallette.darkgray, (x, 0), (x, height))

    for y in range(0, height, gridSize):
        pygame.draw.line(screen, pallette.darkgray, (0, y), (width, y))

    #Draw visible tiles
    for x in visibleXRange:
        for y in visibleYRange:
            #check the dictionary for a defined tile
            if (x, y) in mapTiles:
                pygame.draw.rect(screen, pallette.orange, ((x + int(xOffset)) * gridSize, -(y - int(yOffset)) * gridSize, gridSize, gridSize))
    
    #Show data of the tile the mouse is hovering over
    mousePos = pygame.mouse.get_pos()
    mouseTile = windowPosToTile(mousePos[0], mousePos[1], xOffset, yOffset)

    #check if the mouse is hovering over a tile and display the info near the mouse
    if mouseTile in mapTiles:
        
        #Generate string to display
        text = ""

        #Add the system Position
        text += "Position: (" + str(mouseTile[0]) + ", " + str(mouseTile[1]) + ")\n"

        #Add the system sector
        sectorName = mapTiles[mouseTile][0][0].split("-")[0]
        text += "Sector: " + sectorName + "\n"

        #Add the system name
        systemName = mapTiles[mouseTile][0][0].split("-")[1]
        text += "System: " + systemName + "\n"

        text += "Waypoints:\n"

        #Check for multiple waypoints
        if len(mapTiles[mouseTile]) > 1:
            for i in range(0, len(mapTiles[mouseTile])):
                text += formatWaypoint(mapTiles[mouseTile][i][1]) + " ID: " + mapTiles[mouseTile][i][0].split("-")[2] + "\n"
        else:
            text += formatWaypoint(mapTiles[mouseTile][0][1]) + "\n"

        #Change text offset based on which quadrant the mouse is in
        textXShift = 0
        textYShift = 0

        #Check if the text will go off the screen using the longest line of text

        #Height of the font characters
        fontSize = 16

        #Offset from the mouse
        textOffset = 10

        #Positon for the text to be displayed
        textPos = (mousePos[0] + textOffset, mousePos[1] + textOffset)

        #show the text
        getTextDisplay(text, textPos, "Arial", fontSize, pallette.darkgray, pallette.orange, 4, pallette.white, 10)




    #Show the center grid coordinate
    centerTile = windowPosToTile(width / 2, height / 2, xOffset, yOffset)
    centerTileDisplay = pygame.font.SysFont("Arial", 30).render(str(centerTile), True, pallette.white)
    screen.blit(centerTileDisplay, (10, 10))

    # Flip the display
    pygame.display.flip()
    
    # Limit the frame rate to 60 fps
    clock.tick(60)

# Clean up Pygame
pygame.quit()

print("Map Closed")
