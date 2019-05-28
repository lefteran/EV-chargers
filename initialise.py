import solution as sl
import parameters as pam
import redistribute as rdb
import local_search as ls
import copy
import sys

# def installCP(R, S, k):
# 	if sum(S.r.values()) < R:
# 		S.r[k] += 1
# 	else:
# 		S.st[k] += 1
# 	S.y[k] += 1


def findClosestFacilitiesToVehicles(S, parameters):
	for vehicleKey, _ in parameters.vehiclesDict.items():
		initialFacilityKey = list(parameters.facilitiesDict.keys())[0]
		closest = parameters.timesDict[vehicleKey][initialFacilityKey]
		closestFacility = initialFacilityKey
		for facilityKey, _ in parameters.facilitiesDict.items():
			if parameters.timesDict[vehicleKey][facilityKey] < closest and S.is_open(facilityKey):
				closest = parameters.timesDict[vehicleKey][facilityKey]
				closestFacility = facilityKey
		S.connect(vehicleKey, closestFacility)


def naiveSolution(parameters):
	S = sl.Solution(parameters)
	for _, zoneObject in parameters.zonesDict.items():
		for facilityId in zoneObject.facilities:
			# if facilityId == '26817937':
			# 	a=2
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
			# if facilityId == '26817937':
			# 	a=2
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
					S.close_facility(facilityId)
					
	print("on-street done")
	findClosestFacilitiesToVehicles(S, parameters)
	return S


def initialise(parameters, lambdaVal):
	initSol = naiveSolution(parameters)
	# print("------------------ INITIAL SOLUTION (lambda = %.2f) ----------------------" %lambdaVal)
	# initSol.printSol(parameters, lambdaVal)
	if initSol.isFeasibleWithoutBudget(parameters):
		print("solution is feasible without budget")
	else:
		print("not feasible")
		# ls.reduceCPs(parameters, initSol)
		# for zone in parameters.zones:
		# 	zoneFacilities = zone.facilities
		# 	rdb.redistributeCPs(initSol, zoneFacilities)
	return initSol