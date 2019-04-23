import solution as sl
import parameters as pam
import redistribute as rdb
import local_search as ls
import copy

def installCP(R, S, k):
	if sum(S.r) < R:
		S.r[k] += 1
	else:
		S.st[k] += 1
	S.y[k] += 1


def findClosestFacilitiesToVehicles(S, parameters):
	for i in range(parameters.Nov):
		closest = parameters.distMatrix[i][0]
		closestFac = 0
		for j in range(parameters.Nof):
			if parameters.distMatrix[i][j] < closest:
				closest = parameters.distMatrix[i][j]
				closestFac = j
		S.connect(i, closestFac)


def naiveSolution(parameters):
	S = sl.Solution(parameters)
	for zone in parameters.zones:
		for facility in zone.facilities:
			if facility.alpha == 0:								# open off-street facilities first
				k = facility.id
				while S.y[k] < facility.capacity:
					installCP(parameters.R, S, k)
	for zone in parameters.zones:
		z = zone.id
		for facility in zone.facilities:
			if facility.alpha == 1:								# open on-street facilities
				k = facility.id
				if S.zoneOnstreetCPs(zone.facilities) < zone.onStreetBound:
					while (S.y[k] < facility.capacity) and (S.zoneOnstreetCPs(zone.facilities) < zone.onStreetBound):
						installCP(parameters.R, S, k)
	findClosestFacilitiesToVehicles(S, parameters)
	return S


def initialise(parameters, lambdaVal):
	initSol = naiveSolution(parameters)
	print("------------------ INITIAL SOLUTION (lambda = %.2f) ----------------------" %lambdaVal)
	initSol.printSol(parameters, lambdaVal)
	if initSol.isFeasibleWithoutBudget(parameters):
		ls.reduceCPs(parameters, initSol)
		for zone in parameters.zones:
			zoneFacilities = zone.facilities
			rdb.redistributeCPs(initSol, zoneFacilities)
	return initSol