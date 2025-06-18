import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import copy
import os
import time

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def calculatePixelLocation(point):
    rowList = np.linspace(-1 * overallRadius - padding, overallRadius + padding, planeResolutionX)
    columnList = np.linspace(-1 * overallRadius - padding, overallRadius + padding, planeResolutionY)

    row = 0
    column = 0

    for i, val in enumerate(rowList):
        if val >= point.x:
            row = i
            break

    for i, val in enumerate(columnList):
        if val >= point.y:
            column = i
            break

    return row, column

def calculatePixelIntensity(pointProjectedDistance, minProjectedDistance, maxProjectedDistance):
    if pointProjectedDistance < minProjectedDistance:
        return 0

    pixelIntensity = (pointProjectedDistance - minProjectedDistance)/(maxProjectedDistance - minProjectedDistance)*21
    return int(pixelIntensity)

def rotatePoint(point, angleX = 0, angleY = 0, angleZ = 0):
    x = point.x
    y = point.y
    z = point.z

    if angleX != 0:
        tempX, tempY, tempZ = (x, y, z)

        x = np.matmul([1, 0, 0], [[tempX], [tempY], [tempZ]])
        y = np.matmul([0, np.cos(angleX), -np.sin(angleX)], [[tempX], [tempY], [tempZ]])
        z = np.matmul([0, np.sin(angleX), np.cos(angleX)], [[tempX], [tempY], [tempZ]])

        x, y, z = (float(x), float(y), float(z))

    if angleY != 0:
        tempX, tempY, tempZ = (x, y, z)

        #print([np.cos(angleY), 0, np.sin(angleY)], [[tempX], [tempY], [tempZ]])

        x = np.matmul([np.cos(angleY), 0, np.sin(angleY)], [[tempX], [tempY], [tempZ]])
        y = np.matmul([0, 1, 0], [[tempX], [tempY], [tempZ]])
        z = np.matmul([-np.sin(angleY), 0, np.cos(angleY)], [[tempX], [tempY], [tempZ]])

        x, y, z = (float(x), float(y), float(z))

    if angleZ != 0:
        tempX, tempY, tempZ = (x, y, z)

        x = np.matmul([np.cos(angleZ), -np.sin(angleZ), 0], [[tempX], [tempY], [tempZ]])
        y = np.matmul([np.sin(angleZ), np.cos(angleZ), 0], [[tempX], [tempY], [tempZ]])
        z = np.matmul([0, 0, 1], [[tempX], [tempY], [tempZ]])

        x, y, z = (float(x), float(y), float(z))

    return Point(x, y, z)

numberPoints = 70
theta = np.linspace(0, 2*np.pi, numberPoints)
radius = 4
branchRadius = 2.4
overallRadius = radius + branchRadius

planeResolutionX = 30
planeResolutionY = 30
padding = 2 # should not be 0
planeZ = 12 # z = planeZ is the equation of the plane

asciiValues = ".:-=~+*oO0#%$@&BW8M&$@"

index = 0
loop = 0
numLoop = 3

while loop < numLoop:

    mainCircle = [rotatePoint(Point(radius*np.cos(theta[i]), radius*np.sin(theta[i]), 0), angleX = theta[index], angleY = theta[index]) for i in range(numberPoints)]

    projectedPlane = []

    minProjectedDistance = np.inf
    maxProjectedDistance = -np.inf


    for i in range(planeResolutionY):
        projectedPlane.append([0]*planeResolutionX)


    for i in range(numberPoints):
        nonOrientedCircle = [Point(0, branchRadius*np.sin(theta[j]), branchRadius*np.cos(theta[j])) for j in range(numberPoints)]

        angle = np.arctan(mainCircle[i].y/mainCircle[i].x)

        for j in range(numberPoints):
            cosAngle = np.cos(angle - np.pi/2)
            sinAngle = np.sin(-angle - np.pi/2)

            x = np.matmul([cosAngle, -sinAngle], [[nonOrientedCircle[j].x], [nonOrientedCircle[j].y]])
            y = np.matmul([sinAngle, cosAngle], [[nonOrientedCircle[j].x], [nonOrientedCircle[j].y]])
            z = nonOrientedCircle[j].z

            point = Point(x + mainCircle[i].x, y + mainCircle[i].y, z + mainCircle[i].z)

            projectedDistance = 1 / (planeZ - point.z)

            if projectedDistance > maxProjectedDistance:
                maxProjectedDistance = projectedDistance

            if projectedDistance < minProjectedDistance:
                minProjectedDistance = projectedDistance

            row, column = calculatePixelLocation(point)
            projectedPlane[row][column] = max(projectedDistance, projectedPlane[row][column])

    os.system("clear")

    for i in range(planeResolutionX):
        for j in range(planeResolutionY):
            projectedPlane[i][j] = calculatePixelIntensity(projectedPlane[i][j], minProjectedDistance, maxProjectedDistance)
            print(asciiValues[projectedPlane[i][j]], end="")
            print(asciiValues[projectedPlane[i][j]], end="")

        print()

    index += 1

    if index == numberPoints:
        loop += 1
        index = 0

