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


def swap(S, openFacIds, closedFacIds):
	newS = copy.deepcopy(S)
	# openNewFacilities(newS, facilities, closedFacIds, standard, rapid, totalCPs)
	# closeOldFacilities(newS, openFacIds)


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

# def getZoneNeighborhood(zone, parameters, S):




# def getTotalZoneCPs(S, zoneFaciities):
# 	standard = 0
# 	rapid = 0
# 	for facility in zoneFaciities:
# 		facId = facility.id
# 		standard += S.st[facId]
# 		rapid += S.r[facId]
# 	return standard, rapid


# # Returns a sorted list where each entry is a tuple of a dictionary (facId, remaining capacity)
# def remainingCapacities(S, zoneFaciities):
# 	remainingCap = {}
# 	for facility in zoneFaciities:
# 		facId = facility.id
# 		remainingCap[facId] = facility.capacity - S.y[facId]
# 	remCapSorted = sorted(remainingCap.items(), key = lambda remCap:(remCap[1], remCap[0]), reverse=True)
# 	return remCapSorted



def isFacilityFull(S, facility):
	return S.y[facility.id] == facility.capacity

# def isFacilityEmpty(S, facility):
# 	return S.y[facility.id] == 0

def hasFacilityStandardCPs(S, facId):
	return S.st[facId] != 0

def hasFacilityRapidCPs(S, facId):
	return S.r[facId] != 0

def getNextNonFullFac(S, sortedByCapacity, index):
	for i in range(index, len(sortedByCapacity)):
		facility = sortedByCapacity[i]
		if not isFacilityFull(S, facility):
			return sortedByCapacity[i]

def redistributeCPs(S, zoneFacilities):
	sortedByCapacity = sorted(zoneFacilities, key=lambda x: x.capacity, reverse=True)
	index = 0
	facilityToFill = getNextNonFullFac(S, sortedByCapacity, index)
	for facilityToEmpty in sortedByCapacity[::-1]:
		standardFacsToMove = S.st[facilityToEmpty.id]
		rapidFacsToMove = S.r[facilityToEmpty.id]
		for i in range(standardFacsToMove):
			S.increaseStandardCP(facilityToFill.id)
			S.removeStandardCP(facilityToEmpty.id)
			if (not hasFacilityStandardCPs(S, facilityToEmpty.id)) and (not hasFacilityRapidCPs(S, facilityToEmpty.id)):
				S.close_facility(facilityToEmpty.id)
			if isFacilityFull(S, facilityToFill):
				facilityToFill = getNextNonFullFac(S, sortedByCapacity, index)
			if facilityToEmpty.id == facilityToFill.id:
				break
		for i in range(rapidFacsToMove):
			S.increaseRapidCP(facilityToFill.id)
			S.removeRapidCP(facilityToEmpty.id)
			if (not hasFacilityStandardCPs(S, facilityToEmpty.id)) and (not hasFacilityRapidCPs(S, facilityToEmpty.id)):
				S.close_facility(facilityToEmpty)
			if isFacilityFull(S, facilityToFill):
				facilityToFill = getNextNonFullFac(S, sortedByCapacity, index)
			if facilityToEmpty.id == facilityToFill.id:
				break



# Returns a list of open and a list of closed facility ids in the given zone
def getOpenAndClosedFacIds(S, zone):
	openFacs = []
	closedFacs = []
	facilities = zone.facilities
	for facility in facilities:
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



# def getSolWithClosedFacs(S, facilities):
# 	for facility in facilities:



# def localSearch(S, parameters, zones):
# 	zonesFlags = [True] * parameters.Noz
# 	flag = True
# 	while flag:
# 		for zone in zones:


# def checkCPs(newS):				
