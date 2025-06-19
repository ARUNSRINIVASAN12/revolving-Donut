import multiprocessing
import test2
import threading
import numpy as np
import time
import sys

theta = np.linspace(0, 2*np.pi, test2.numberPoints)

numCores = multiprocessing.cpu_count() - 3

potentError = 0

def printDonutFrames(planes):
    for index, plane in enumerate(planes):
        print("\033[H", end="")

        for i in range(int(test2.planeResolutionX)):
            for j in range(int(test2.planeResolutionY)):
                print(test2.asciiValues[int(plane[i][j])], end="")
                print(test2.asciiValues[int(plane[i][j])], end="")

            print()

        if index != len(planes) - 1:
            time.sleep(0.08)

printThread = None
numLoop = 6

for loop in range(numLoop):
    for i in range(test2.numberPoints//numCores + 1):
        angles = theta[int(i*numCores): min(int((i+1)*numCores), test2.numberPoints-1)]

        with multiprocessing.Pool(processes= numCores) as pool:
            orderedProjectedPlanes = pool.map(test2.printDonut, angles)

        if printThread is not None:
            printThread.join()

        printThread = threading.Thread(target= printDonutFrames, args= (orderedProjectedPlanes,))
        printThread.start()




