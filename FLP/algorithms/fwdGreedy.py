import settings
import _pickle as pickle
from tqdm import tqdm


def invertDict(originalDict):
    invertedDict = {}
    for k, v in originalDict.items():
        invertedDict[v] = invertedDict.get(v, [])
        invertedDict[v].append(k)
    return invertedDict



def getTimeWithNewFacility(S, facilityId):
    totalTime = 0
    for _,vehicleObj in settings.parameters.vehiclesDict.items():
        facilities = pickle.loads(pickle.dumps(S, -1))
        facilities.append(facilityId)
        totalTime += vehicleObj.getNearestFacilityTime(facilities)
    return totalTime



def forwardGreedy():
    print("Running forward greedy ...")
    S = []
    totalTime = float("inf")
    # while len(S) < settings.parameters.k:
    for iteration in tqdm(range(settings.parameters.k)):
        totalTime = float("inf")
        minTimeFacility = None
        # for facilityKey, _ in settings.parameters.facilitiesDict.items():
        for facilityId in settings.parameters.candidateLocations:
            if facilityId not in S:
                timeWithNewFacility = getTimeWithNewFacility(S, facilityId)
                if timeWithNewFacility < totalTime:
                    totalTime = timeWithNewFacility
                    minTimeFacility = facilityId
        S.append(minTimeFacility)
    return S,totalTime






