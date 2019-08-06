# LIBRARIES
import _pickle as pickle
# FILES
import settings
import i_o.serializationIO as serializationIO


def computeTime(S):
    totalTime = 0
    for _, vehicleObj in settings.vehiclesDict.items():
        vehicleToFacilityTime = vehicleObj.getTimeToNearestFacility(S)
        totalTime += vehicleToFacilityTime
    return totalTime


def localSearch():
    print(f"Running local search with {settings.numberOfVehicles} vehicles and {settings.radius} radius ...")
    solObject = serializationIO.importAndDeserialize(settings.fwdGreedyFile)
    S = solObject.solutionList
    bestTime = solObject.cost
    Closed = list(set(settings.candidateLocations).difference(set(S)))
    flag = True

    while flag:
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
        if not betterSolution:
            return S, bestTime

