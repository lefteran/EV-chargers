import itertools
import copy

def combinations(L, p):
	combs = []
	for subset in itertools.combinations(L, p):
		combs.append(list(subset))
	return combs


def isSwapFeasible(S, facilities, openfacIds, closedFacIds):
	totalSt, totalRap, totalCPs = 0, 0, 0
	openCPs = 0
	closedTotalCap = 0
	for facId in openfacIds:
		openCPs += S.y[facId]
	for facId in closedFacIds:
		for facility in facilities:
			if facility.id == facId:
				closedTotalCap += facility.capacity
	if closedTotalCap < openCPs:
		return False
	else:
		return True	


def openNewFacilities(newS, facilities, closedFacIds, standard, rapid, totalCPs):
	L = sorted(facilities, key=lambda x: x.capacity, reverse=True)
	for facility in L:
		facId = facility.id
		capacity = facility.capacity
		if rapid >= capacity:
			newS.r[facId] = capacity
			rapid -= capacity

			newS.st[facId] = 0
			
			newS.y[facId] = capacity
			totalCPs -= capacity
		
		elif rapid + standard >= capacity:
			newS.r[facId] = rapid
			rapid = 0
		
			remaining = capacity - rapid
			newS.st[facId] = remaining
			standard -= remaining
		
			newS.y[facId] = capacity
			totalCPs -= capacity

		elif rapid + standard < capacity:
			newS.r[facId] = rapid
			rapid = 0
		
			newS.st[facId] = standard
			standard = 0
		
			total = rapid + standard
			newS.y[facId] = total
			totalCPs -= total
			break


def closeOldFacilities(newS, openFacIds):
	for facId in openFacIds:
		newS.close_facility(facId)

def swapFacilities(S, parameters, openFacIds, closedFacIds):
	newS = copy.deepcopy(S)
	standard, rapid = getFacsCPs(S, openFacIds)
	openNewFacilities(newS, parameters.facilities, closedFacIds, standard, rapid, standard + rapid)
	closeOldFacilities(newS, openFacIds)
	return newS

# Returns the numbers of standard and rapid CPs for the list of facility ids
def getFacsCPs(S, facIds):
	standard = 0
	rapid = 0
	for facId in facIds:
		standard += S.st[facId]
		rapid += S.r[facId]
	return standard, rapid


# Returns a list of open and a list of closed facility ids in the given zone
def getOpenAndClosedFacIds(S, zone):
	openFacs = []
	closedFacs = []
	for facility in zone.facilities:
		facid = facility.id
		openFacs.append(facid) if S.is_open(facid) else closedFacs.append(facid)
	return openFacs, closedFacs


# Removes as many rapid and standard CPs until the solution is infeasible
def reduceCPs(parameters, S):
	for facility in parameters.facilities:
		facId = facility.id
		for i in range(S.r[facId]):
			S.removeRapidCP(facId)
			if not S.isFeasibleWithoutBudget(parameters):
				S.increaseRapidCP(facId)
				break
		for i in range(S.st[facId]):
			S.removeStandardCP(facId)
			if not S.isFeasibleWithoutBudget(parameters):
				S.increaseStandardCP(facId)
				break


def getZoneNewSolution(S, parameters, zone):
	lambdaVal = 0
	newS = S
	openFacs, closedFacs = getOpenAndClosedFacIds(S, zone)
	openFacCombs = combinations(openFacs, parameters.swaps)
	closedFacCombs = combinations(closedFacs, parameters.swaps)
	allSwaps = list(itertools.product(openFacCombs, closedFacCombs))
	for swap in allSwaps:
		if isSwapFeasible(S, parameters.facilities, swap[0], swap[1]):
			oldCost = S.getCostLagrangian(parameters, lambdaVal)
			newS = swapFacilities(S, parameters, swap[0], swap[1])
			newCost = newS.getCostLagrangian(parameters, lambdaVal)
			if newCost < oldCost:
				break
	return newS


def localSearch(S, parameters):
	for zone in parameters.zones:
		flag = True
		while flag:
			newS = getZoneNewSolution(S, parameters, zone)
			if newS == S:
				flag = False
			else:
				S = newS
	return newS