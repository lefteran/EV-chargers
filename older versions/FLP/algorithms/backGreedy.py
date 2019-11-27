# LIBRARIES
from tqdm import tqdm
from os import cpu_count
from multiprocessing import Process, Lock, Manager
from math import floor
# FILES
import settings

# def vehiclesClosestFacilitiesDict(facilities):
#     closestFacilitiesDict = {}
#     for vehicleKey, vehicleObj in settings.vehiclesDict.items():
#         closestFacility =  vehicleObj.getNearestFacility(facilities)
#         closestFacilitiesDict[vehicleKey] = closestFacility
#     return closestFacilitiesDict


def getVehiclesListTuples():
    for vehicleKey, vehicleObj in settings.vehiclesDict.items():
        settings.vehiclesClosestTuples[vehicleKey] = vehicleObj.getClosestFacilities_TimesTuples()


# def removeFacilityFromTupleLists(facilityToRemove):
#     for vehicleKey, vehicleObj in settings.vehiclesDict.items():
#         for facilityTuple in settings.vehiclesClosestTuples[vehicleKey]:
#             if settings.vehiclesClosestTuples[vehicleKey][1] == facilityToRemove:
#                 settings.vehiclesClosestTuples[vehicleKey].remove(facilityTuple)
#                 return


def getTimeWithoutGivenFacility(S, facilityId):
    totalTime = 0
    S.remove(facilityId)
    for vehicleKey, vehicleObj in settings.vehiclesDict.items():
        for closestTuple in settings.vehiclesClosestTuples[vehicleKey]:
        # closestTuple = settings.vehiclesClosestTuples[vehicleKey][0]
            if closestTuple[0] not in settings.removedFacilityIds:
                timeToFacility = closestTuple[1]
                break
        totalTime += timeToFacility
    S.append(facilityId)
    return totalTime



def removeLeastImportantFacility(S, previousTotalTime):
    totalTime = float("inf")
    minTimeFacility = None
    count = 0
    for facilityKey in S:
        count += 1
        timeWithoutGivenFacility = getTimeWithoutGivenFacility(S, facilityKey)
        if timeWithoutGivenFacility < totalTime:
            totalTime = timeWithoutGivenFacility
            minTimeFacility = facilityKey
    settings.removedFacilityIds.append(minTimeFacility)
    S.remove(minTimeFacility)
    return totalTime



# def getTimesForFacilitiesToCheck(S, previousTotalTime, facilitiesToCheck, timeWithoutFacilityDict, lock):
#     totalTime = previousTotalTime
#     for facilityKey in facilitiesToCheck:
#         timeWithoutGivenFacility = getTimeWithoutGivenFacility(S, facilityKey)
#         if timeWithoutGivenFacility < totalTime:
#             totalTime = timeWithoutGivenFacility
#         lock.acquire()
#         timeWithoutFacilityDict[facilityKey] = totalTime
#         lock.release()
#
#
# def removeLeastImportantFacilityParallel(S, previousTotalTime):
#     numberOfProcesses = cpu_count()
#     # numberOfProcesses = 1
#     manager = Manager()
#     lock = manager.Lock()
#     timeWithoutFacilityDict = manager.dict()
#     processes = []
#     SLength = len(S)
#     facilityKeysPerProcess = floor(SLength / numberOfProcesses)
#
#     for i in range(numberOfProcesses):
#         first = i * facilityKeysPerProcess
#         last = None if i == numberOfProcesses -1 else first + facilityKeysPerProcess
#         facilitiesToCheck = S[first:last]
#         process = Process(target=getTimesForFacilitiesToCheck, args=(S, previousTotalTime, facilitiesToCheck, timeWithoutFacilityDict, lock))
#         processes.append(process)
#         process.start()
#     for process in processes:
#         process.join()
#
#     minimumTime = float("inf")
#     facilityToRemove = None
#     for facilityKey, timeWithoutFacilityKey in timeWithoutFacilityDict.items():
#         if timeWithoutFacilityKey < minimumTime:
#             minimumTime = timeWithoutFacilityKey
#             facilityToRemove = facilityKey
#     settings.removedFacilityIds.append(facilityToRemove)
#     S.remove(facilityToRemove)
#     return minimumTime




def backwardGreedy():
    print(f"Running backward greedy with {settings.numberOfVehicles} vehicles and {settings.radius} radius ...")
    S = settings.candidateLocations
    iterations = len(S) - settings.k
    totalTime = float("inf")
    getVehiclesListTuples()
    for _ in tqdm(range(iterations)):
        previousTotalTime = totalTime
        totalTime = removeLeastImportantFacility(S, previousTotalTime)
    return S,totalTime