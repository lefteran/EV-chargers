import solution.solution as sl

def combinePartsIntoOneSolution(globalPart, localPartDict, parameters):
    S = sl.Solution(parameters)
    for vehicleKey, _ in parameters.vehiclesDict.items():
        S.x[vehicleKey] = globalPart[vehicleKey]
    for zoneKey, _ in localPartDict.items():
        for facilityId in parameters.zonesDict[zoneKey].facilities:
            S.omega[facilityId] = localPartDict[zoneKey].omega[facilityId]
            S.st[facilityId] = localPartDict[zoneKey].st[facilityId]
            S.r[facilityId] = localPartDict[zoneKey].r[facilityId]
            S.y[facilityId] = localPartDict[zoneKey].y[facilityId]
    return S
