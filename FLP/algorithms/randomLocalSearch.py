import settings
from tqdm import tqdm
import serializationIO
from random import choice


def computeTime(S):
    totalTime = 0
    for _, vehicleObj in settings.parameters.vehiclesDict.items():
        vehicleToFacilityTime = vehicleObj.getNearestFacilityTime(S)
        totalTime += vehicleToFacilityTime
    return totalTime


def randomLocalSearch():
    solObject = serializationIO.importAndDeserialize("solutions/fwdGreedy_" + str(settings.parameters.k) + ".json")
    S = solObject.solutionList
    bestTime = solObject.cost
    Closed = list(set(settings.parameters.facilitiesDict.keys()).difference(set(S)))

    for randomIteration in range(settings.parameters.r):
        P1 = []
        P2 = []
        for i in range(settings.parameters.p):
            randomOpen = choice(S)
            P1.append(randomOpen)
        for i in range(settings.parameters.p):
            randomClosed = choice(Closed)
            P2.append(randomClosed)
        setS = set(S)
        setP1 = set(P1)
        setP2 = set(P2)
        candidateSol =  list((setS.difference(setP1)).union(setP2))
        newTime = computeTime(candidateSol)
        if newTime< bestTime:
            S = candidateSol
            bestTime = newTime
    return S, bestTime
