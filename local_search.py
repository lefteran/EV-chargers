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
# *** THE FOLLOWING METHOD TO BE MOVED INSIDE SOLUTION CLASS ***
def reduceCPs(parameters, S):
	count = 0
	total = len(parameters.facilitiesDict)
	for facilityKey, _ in parameters.facilitiesDict.items():
		count += 1
		print("facility %d of %d" %(count, total))
		for i in range(S.r[facilityKey]):
			S.removeRapidCP(facilityKey)
			if not S.isFeasibleWithReducedCPs(parameters, facilityKey):
				S.increaseRapidCP(facilityKey)
				break
		for i in range(S.st[facilityKey]):
			S.removeStandardCP(facilityKey)
			if not S.isFeasibleWithReducedCPs(parameters, facilityKey):
				S.increaseStandardCP(facilityKey)
				break


# Returns a new solution swapping between a set of open and a set of closed facilities for a given zone
def getZoneNewSolution(S, parameters, zone, lambdaVal):
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


# ############################ GLOBAL SWAPS LOCAL SEARCH ####################################

# def hasOpenFacility(S, comb):
# 	for facId in comb:
# 		if S.is_open(facId):
# 			return True
# 	return False

# def hasClosedFacility(S, comb):
# 	for facId in comb:
# 		if not S.is_open(facId):
# 			return True
# 	return False

# def swapFacilitiesGlobally(S, parameters):
# 	newS = copy.deepcopy(S)
# 	# standard, rapid = getFacsCPs(S, openFacIds)
	
# 	return newS


# def calculateZoneDemand(parameters, S, z):
# 	currentZoneDemand = 0
# 	for facility in parameters.facilities:
# 		if facility.id == z and S.is_open(facility.id):
# 			currentZoneDemand += S.y[facility.id]
# 	return currentZoneDemand



# def isSolZoneFeasible(parameters, S, zone):
# 	totalZoneDemand = 0
# 	for adjZoneId in zone.adjacent:
# 		totalZoneDemand += calculateZoneDemand(parameters, S, adjZoneId)
# 	if totalZoneDemand < parameters.gamma * zone.demand:
# 		return False


# def getNewSolution(parameters, S, facilitiesToOpen, facilitiesToClose):
# 	newS = copy.deepcopy(S)
# 	rapid = 0
# 	standard = 0
# 	total = 0
# 	for facilityToClose in facilitiesToClose:
# 		if newS.is_open(facilityToClose):
# 			rapid += newS.r[facilityToClose]
# 			standard += newS.st[facilityToClose]
# 			total += newS.y[facilityToClose]
# 			newS.close_facility(facilityToClose)

#  	Lcap = sorted(facilitiesToOpen, key=lambda x: x.capacity, reverse=True)





	# for facilityToOpen in facilitiesToOpen:
	# 	facilityId = facilitiesToOpen.id
		# if not newS.is_open(facilityId):
			



	
# def getZoneNewSolutionGlobally(S, parameters, zone, lambdaVal):
# 	# TO CHECK BELOW PSEUDOCODE
# 	newS = S
# 	allCombs = combinations(parameters.facilities , parameters.swaps)
# 	for facsToAdd in allCombs:
# 		for facsToRemove in allCombs:
# 			if facsToAdd != facsToRemove\
# 			and hasClosedFacility(S, facsToAdd)\
# 			and hasOpenFacility(S, facsToRemove):
# 				if isSwapFeasibleGlobally(S):
# 					oldCost = S.getCostLagrangian(parameters, lambdaVal)
# 					newS = swapFacilities(S, parameters, facsToAdd, facsToRemove)
# 					newCost = newS.getCostLagrangian(parameters, lambdaVal)
# 					if newCost < oldCost:
# 						break
# 	return newS

# ####################################################################################

def localSearch(S, parameters, lambdaVal):
	for zone in parameters.zones:
		flag = True
		while flag:
			newS = getZoneNewSolution(S, parameters, zone, lambdaVal)
			if newS == S:
				flag = False
			else:
				S = newS
	return newS