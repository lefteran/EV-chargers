import settings
from tqdm import tqdm

# def vehiclesClosestFacilitiesDict(facilities):
#     closestFacilitiesDict = {}
#     for vehicleKey, vehicleObj in settings.parameters.vehiclesDict.items():
#         closestFacility =  vehicleObj.getNearestFacility(facilities)
#         closestFacilitiesDict[vehicleKey] = closestFacility
#     return closestFacilitiesDict


def getVehiclesListTuples():
    for vehicleKey, vehicleObj in settings.parameters.vehiclesDict.items():
        settings.parameters.vehiclesClosestTuples[vehicleKey] = vehicleObj.getClosestFacilities_TimesTuples()


# def removeFacilityFromTupleLists(facilityToRemove):
#     for vehicleKey, vehicleObj in settings.parameters.vehiclesDict.items():
#         for facilityTuple in settings.parameters.vehiclesClosestTuples[vehicleKey]:
#             if settings.parameters.vehiclesClosestTuples[vehicleKey][1] == facilityToRemove:
#                 settings.parameters.vehiclesClosestTuples[vehicleKey].remove(facilityTuple)
#                 return


def getTimeWithoutGivenFacility(S, facilityId):
    totalTime = 0
    S.remove(facilityId)
    for vehicleKey, vehicleObj in settings.parameters.vehiclesDict.items():
        for closestTuple in settings.parameters.vehiclesClosestTuples[vehicleKey]:
        # closestTuple = settings.parameters.vehiclesClosestTuples[vehicleKey][0]
            if closestTuple[0] not in settings.parameters.removedFacilityIds:
                timeToFacility = closestTuple[1]
                break
        totalTime += timeToFacility
    S.append(facilityId)
    return totalTime



def removeLeastImportantFacility(S):
    totalTime = float("inf")
    minTimeFacility = None
    count = 0
    for facilityKey in S:
        count += 1
        timeWithoutGivenFacility = getTimeWithoutGivenFacility(S, facilityKey)
        if timeWithoutGivenFacility < totalTime:
            totalTime = timeWithoutGivenFacility
            minTimeFacility = facilityKey
    settings.parameters.removedFacilityIds.append(minTimeFacility)
    S.remove(minTimeFacility)


def reverseGreedy():
    print("Running reverse greedy ...")
    S = list(settings.parameters.facilitiesDict.keys())
    iterations = len(S) - settings.parameters.k
    totalTime = float("inf")
    getVehiclesListTuples()
    # while len(S) > settings.parameters.k:
    count = 0
    for iteration in tqdm(range(iterations)):
        count += 1
        removeLeastImportantFacility(S)
    return S,totalTime