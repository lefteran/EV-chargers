# LIBRARIES
import _pickle as pickle
from tqdm import tqdm
# FILES
import settings

def invertDict(originalDict):
    invertedDict = {}
    for k, v in originalDict.items():
        invertedDict[v] = invertedDict.get(v, [])
        invertedDict[v].append(k)
    return invertedDict



def getTimeWithNewFacility(S, facilityId):
    totalTime = 0
    facilities = pickle.loads(pickle.dumps(S, -1))
    facilities.append(facilityId)
    for _,vehicleObj in settings.vehiclesDict.items():
        totalTime += vehicleObj.getTimeToNearestFacility(facilities)
    return totalTime


def addMostImportantFacility(S, previousTotalTime):
    totalTime = previousTotalTime
    minTimeFacility = None
    for facilityId in settings.candidateLocations:
        if facilityId not in S:
            timeWithNewFacility = getTimeWithNewFacility(S, facilityId)
            if timeWithNewFacility < totalTime:
                totalTime = timeWithNewFacility
                minTimeFacility = facilityId
    if minTimeFacility is not None:
        S.append(minTimeFacility)
    return totalTime


def forwardGreedy():
    print(f"Running forward greedy with {settings.numberOfVehicles} vehicles and {settings.radius} radius ...")
    S = []
    totalTime = float("inf")
    for _ in tqdm(range(settings.k)):
        previousTotalTime = totalTime
        totalTime = addMostImportantFacility(S, previousTotalTime)
    return S,totalTime






