import solution.solution as sl
import solution.local_search as ls
import copy
# import sys
import _pickle as pickle

# CALL THE METHOD getClosestFacilityToVehicle() FROM THE SOLUTION CLASS INSTEAD OF THE CODE BELOW
def findClosestFacilitiesToVehicles(S, parameters):
	for vehicleKey, _ in parameters.vehiclesDict.items():
		initialFacilityKey = list(parameters.facilitiesDict.keys())[0]
		closest = parameters.timesDict[vehicleKey][initialFacilityKey]
		closestFacility = initialFacilityKey
		for facilityKey, _ in parameters.facilitiesDict.items():
			if facilityKey == '387571819':
				a=2
			if parameters.timesDict[vehicleKey][facilityKey] < closest and S.is_open(facilityKey):
				closest = parameters.timesDict[vehicleKey][facilityKey]
				closestFacility = facilityKey
		S.connect(vehicleKey, closestFacility)


# TO BE MOVED INSIDE THE SOLUTION CLASS
def naiveSolution(parameters):
	S = sl.Solution(parameters)
	for _, zoneObject in parameters.zonesDict.items():
		for facilityId in zoneObject.facilities:
			facility = parameters.facilitiesDict[facilityId]
			if facility.alpha == 0:								# open off-street facilities first
				currentRapid = sum(S.r.values())
				rapidToAdd = min(facility.capacity - S.y[facilityId], parameters.R - currentRapid)
				S.r[facilityId] += rapidToAdd
				S.y[facilityId] += rapidToAdd
				standardToAdd = facility.capacity - S.y[facilityId]
				S.st[facilityId] += standardToAdd
				S.y[facilityId] += standardToAdd
	print("off-street done")
	for _, zoneObject in parameters.zonesDict.items():
		for facilityId in zoneObject.facilities:
			facility = parameters.facilitiesDict[facilityId]
			if facility.alpha == 1:								# open on-street facilities
				currentRapid = sum(S.r.values())
				currentOnStreet = S.zoneOnstreetCPs(zoneObject.facilities, parameters.facilitiesDict)
				rapidToAdd =\
				min(facility.capacity - S.y[facilityId], parameters.R - currentRapid, zoneObject.onStreetBound - currentOnStreet)
				S.r[facilityId] += rapidToAdd
				S.y[facilityId] += rapidToAdd
				currentOnStreet += rapidToAdd
				standardToAdd = min(facility.capacity - S.y[facilityId], zoneObject.onStreetBound - currentOnStreet)
				S.st[facilityId] += standardToAdd
				S.y[facilityId] += standardToAdd
				if S.y[facilityId] == 0:
					S.closeFacility(facilityId)
	print("on-street done")
	findClosestFacilitiesToVehicles(S, parameters)
	return S

def getFacilitiesListByIds(parameters, listOfIds):
	facilitiesList = []
	for facilityId in listOfIds:
		facilitiesList.append(parameters.facilitiesDict[facilityId])
	return facilitiesList


# IMPORT SOLUTION OBJECT FROM FILE
def importSolutionObject(filename):
	with open(filename, 'rb') as solInput:
		return pickle.load(solInput)


def getLocalSolutionsDict(parameters, initSol):
	localSolutionsDict = {}
	for zoneKey,_ in parameters.zonesDict.items():
		zoneSolution = lsl.localSolution(parameters, zoneKey)


def initialiseSolution(parameters):
	if parameters.importSolution:
		initSol = importSolutionObject('Chicago/initialSolutionFiniteCost.pkl')
	else:
		initSol = naiveSolution(parameters)
		initSol.closeRedundantFacilities(parameters)
		initSol.reduceCPs(parameters)
		for _, zoneObject in parameters.zonesDict.items():
			zoneFacilities = getFacilitiesListByIds(parameters, zoneObject.facilities)
			initSol.redistributeCPs(parameters, zoneFacilities)
		if initSol.isFeasibleWithoutBudget(parameters):
			print("solution is feasible without budget")
		else:
			print("not feasible")
		initSol.exportSolutionObject('Chicago/solutionObject.pkl')
	return initSol