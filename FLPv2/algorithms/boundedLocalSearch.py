# LIBRARIES
import _pickle as pickle
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


# FIX PATHS FOR BOUNDED LOCAL SEARCH
def boundedLocalSearch():
    print(f"Running bounded local search with {settings.numberOfVehicles} vehicles and {settings.radius} radius ...")
    solObject = serializationIO.importAndDeserialize(settings.fwdGreedyFile)
    S = solObject.solutionList
    bestTime = solObject.cost
    Closed = list(set(settings.candidateLocations).difference(set(S)))
    flag = True

    for i in tqdm(range(10)):
        betterSolution = False
        for openFacility in S:
            for closedFacility in Closed:
                candidateSol = pickle.loads(pickle.dumps(S, -1))
                candidateSol.remove(openFacility)
                candidateSol.append(closedFacility)
                newTime = computeTime(candidateSol)
                if newTime < bestTime:
                    S = candidateSol
                    bestTime = newTime
                    betterSolution = True
                    break
            if betterSolution:
                break
    return S, bestTime

