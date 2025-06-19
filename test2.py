import numpy as np

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def calculatePixelLocation(point):
    row = 0
    column = 0

    for i, val in enumerate(rowPixelList):
        if val >= point.x:
            row = i
            break

    for i, val in enumerate(columnPixelList):
        if val >= point.y:
            column = i
            break

    return row, column

def calculatePixelIntensity(pointProjectedDistance, minProjectedDistance, maxProjectedDistance):
    if pointProjectedDistance < minProjectedDistance:
        return 0

    pixelIntensity = (pointProjectedDistance - minProjectedDistance)/(maxProjectedDistance - minProjectedDistance)*asciiLength
    return int(pixelIntensity)

def rotatePoint(point, angleX = 0.0, angleY = 0.0, angleZ = 0.0):
    x = point.x
    y = point.y
    z = point.z

    if angleX != 0:
        tempX, tempY, tempZ = (x, y, z)

        x = tempX
        y = np.matmul([np.cos(angleX), -np.sin(angleX)], [[tempY], [tempZ]])
        z = np.matmul([np.sin(angleX), np.cos(angleX)], [[tempY], [tempZ]])

        x, y, z = (float(x), y[0], z[0])

    if angleY != 0:
        tempX, tempY, tempZ = (x, y, z)

        x = np.matmul([np.cos(angleY), np.sin(angleY)], [[tempX], [tempZ]])
        y = tempY
        z = np.matmul([-np.sin(angleY), np.cos(angleY)], [[tempX], [tempZ]])

        x, y, z = (x[0], float(y), z[0])

    if angleZ != 0:
        tempX, tempY, tempZ = (x, y, z)

        x = np.matmul([np.cos(angleZ), -np.sin(angleZ)], [[tempX], [tempY]])
        y = np.matmul([np.sin(angleZ), np.cos(angleZ)], [[tempX], [tempY]])
        z = tempZ

        x, y, z = (x[0], y[0], float(z))

    return Point(x, y, z)

numberPoints = 50
theta = np.linspace(0, 2*np.pi, numberPoints)
radius = 4
branchRadius = 2.1
overallRadius = radius + branchRadius

planeResolutionX = 30
planeResolutionY = 30
padding = 2 # should not be 0
planeZ = 12 # z = planeZ is the equation of the plane where the donut is projected

asciiValues = ' .`^":;!~+-i|/lftxX0#MW&@'
asciiLength = len(asciiValues) - 1

rowPixelList = np.linspace(-1 * overallRadius - padding, overallRadius + padding, planeResolutionX)
columnPixelList = np.linspace(-1 * overallRadius - padding, overallRadius + padding, planeResolutionY)

def printDonut(angleX):
    mainCircle = [Point(radius*np.cos(theta[i]), radius*np.sin(theta[i]), 0) for i in range(numberPoints)]

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

            point = Point(x[0] + mainCircle[i].x, y[0] + mainCircle[i].y, z + mainCircle[i].z)

            point = rotatePoint(point, angleX = angleX, angleY = angleX)

            projectedDistance = 1 / (planeZ - point.z)

            if projectedDistance > maxProjectedDistance:
                maxProjectedDistance = projectedDistance

            if projectedDistance < minProjectedDistance:
                minProjectedDistance = projectedDistance

            row, column = calculatePixelLocation(point)
            projectedPlane[row][column] = max(projectedDistance, projectedPlane[row][column])

    for i in range(planeResolutionX):
        for j in range(planeResolutionY):
            projectedPlane[i][j] = calculatePixelIntensity(projectedPlane[i][j], minProjectedDistance, maxProjectedDistance)

    return projectedPlane

