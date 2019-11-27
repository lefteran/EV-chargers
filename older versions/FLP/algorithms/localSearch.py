# LIBRARIES
import _pickle as pickle
from tqdm import tqdm
# FILES
import settings
import i_o.serializationIO as serializationIO


def computeTime(S, newlyAddedFacilityId, removedFacilityId, previousSolutionAccepted):
    totalTime = 0
    for vehicleKey, vehicleObj in settings.vehiclesDict.items():
        # if vehicleKey == '39':
        #     a=2
        # vehicleToFacilityTimeNaive = vehicleObj.getTimeToNearestFacility(S)
        vehicleToFacilityTime = vehicleObj.getTimeToNearestFacility1(S, newlyAddedFacilityId, removedFacilityId, previousSolutionAccepted)
        # if vehicleToFacilityTime != vehicleToFacilityTimeNaive:
        #     a=2
        totalTime += vehicleToFacilityTime
    return totalTime



def localSearch():
    print(f"Running local search with {settings.numberOfVehicles} vehicles and {settings.radius} radius ...")
    for _, vehicleObject in settings.vehiclesDict.items():
        vehicleObject.createSortedListOfTuplesAndDictOfIndices()
    solObject = serializationIO.importAndDeserialize(settings.fwdGreedyFile)
    S = solObject.solutionList
    bestTime = computeTime(S, '', '', False)
    # initialTime = bestTime
    Closed = list(set(settings.candidateLocations).difference(set(S)))
    flag = True
    previousSolutionAccepted = False
    combinationsUsed = []

    while flag:
        betterSolution = False
        for openFacility in S:
            for closedFacility in Closed:
                if {openFacility, closedFacility} not in combinationsUsed:
                    candidateSol = pickle.loads(pickle.dumps(S, -1))
                    candidateSol.remove(openFacility)
                    candidateSol.append(closedFacility)
                    newTime = computeTime(candidateSol, closedFacility, openFacility, previousSolutionAccepted)
                    previousSolutionAccepted = False
                    if newTime < bestTime:
                        combinationsUsed.append({openFacility, closedFacility})
                        previousSolutionAccepted = True
                        S = candidateSol
                        bestTime = newTime
                        betterSolution = True
                        break
            if betterSolution:
                break
        if not betterSolution:
            return S, bestTime



def localSearchOld():
    print(f"Running local search with {settings.numberOfVehicles} vehicles and {settings.radius} radius ...")
    for _, vehicleObject in settings.vehiclesDict.items():
        vehicleObject.createSortedListOfTuplesAndDictOfIndices()

    solObject = serializationIO.importAndDeserialize(settings.fwdGreedyFile)
    S = solObject.solutionList
    bestTime = solObject.cost
    Closed = list(set(settings.candidateLocations).difference(set(S)))
    # serializationIO.serializeAndExport(Closed, 'data/debug.json')
    # Closed = serializationIO.importAndDeserialize('data/debug.json')
    flag = True
    previousSolutionAccepted = False

    while flag:
        betterSolution = False
        for openFacility in S:
            for closedFacility in Closed:
                candidateSol = pickle.loads(pickle.dumps(S, -1))
                candidateSol.remove(openFacility)
                candidateSol.append(closedFacility)
                newTime = computeTime(candidateSol, closedFacility, openFacility, previousSolutionAccepted)
                previousSolutionAccepted = False
                if newTime < bestTime:
                    previousSolutionAccepted = True
                    S = candidateSol
                    bestTime = newTime
                    betterSolution = True
                    break
            if betterSolution:
                break
        if not betterSolution:
            return S, bestTime







def localSearch1():                 # MODIFY THE ABOVE ALGORITHM HERE TO ALLOW GENERALISATION FOR p=2,3. TRY FIRST WITH
                                    # p=1 TO VERIFY IT GIVES THE SAME SOLUTION. TAKE ALL THE POSSIBLE COMBINATIONS OF OPEN
                                    # AND CLOSED FACILITIES
    print(f"Running local search with {settings.numberOfVehicles} vehicles and {settings.radius} radius ...")
    for _, vehicleObject in settings.vehiclesDict.items():
        vehicleObject.createSortedListOfTuplesAndDictOfIndices()

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
                newTime = computeTime(candidateSol, closedFacility, openFacility)
                if newTime < bestTime:
                    S = candidateSol
                    bestTime = newTime
                    betterSolution = True
                    break
            if betterSolution:
                break
        if not betterSolution:
            return S, bestTime


