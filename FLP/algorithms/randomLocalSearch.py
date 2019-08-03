# LIBRARIES
from random import choice
from tqdm import tqdm
# FILES
import settings
import i_o.serializationIO as serializationIO


def computeTime(S):
    totalTime = 0
    for _, vehicleObj in settings.vehiclesDict.items():
        vehicleToFacilityTime = vehicleObj.getTimeToNearestFacility(S)
        totalTime += vehicleToFacilityTime
    return totalTime


def randomLocalSearch():
    print(f"Running random local search with {settings.numberOfVehicles} vehicles and {settings.radius} radius ...")
    solObject = serializationIO.importAndDeserialize(settings.fwdGreedyFile)
    S = solObject.solutionList
    bestTime = solObject.cost
    Closed = list(set(settings.candidateLocations).difference(set(S)))

    for randomIteration in tqdm(range(settings.r)):
        P1 = []         # SET OF FACILITIES TO CLOSE
        P2 = []         # SET OF FACILITIES TO OPEN
        for i in range(settings.p):
            randomOpen = choice(S)
            P1.append(randomOpen)
        for i in range(settings.p):
            randomClosed = choice(Closed)
            P2.append(randomClosed)
        setS = set(S)
        setP1 = set(P1)
        setP2 = set(P2)
        candidateSol =  list((setS.difference(setP1)).union(setP2))
        newTime = computeTime(candidateSol)
        if newTime < bestTime:
            S = candidateSol
            bestTime = newTime
    return S, bestTime
