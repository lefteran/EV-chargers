import itertools
import _pickle as pickle
# import ujson

# def combinations(L, p):
# 	combs = []
# 	for subset in itertools.combinations(L, p):
# 		combs.append(list(subset))
# 	return combs

def combinationsUpToParameter(L, p):
	combs = []
	for i in range(p):
		for subset in itertools.combinations(L, i+1):
			combs.append(list(subset))
	return combs


def isSwapFeasible(S, parameters, openFacilityIds, closedFacilityIds):
	# print("\tchecking if swap is feasible")
	openCPs = 0
	closedTotalCap = 0
	for facilityId in openFacilityIds:
		openCPs += S.y[facilityId]
	for facilityId in closedFacilityIds:
		closedTotalCap += parameters.facilitiesDict[facilityId].capacity
	if closedTotalCap < openCPs:
		return False
	else:
		return True	


def openNewFacilities(newS, parameters, closedFacilityIds, standard, rapid):
	totalCPs = standard + rapid
	L = []
	for facilityId in closedFacilityIds:
		L.append(parameters.facilitiesDict[facilityId])
	L.sort(key=lambda x: x.capacity, reverse=True)
	for facility in L:
		newS.openFacility(facility.id)

		if rapid >= facility.capacity:

			newS.r[facility.id] = facility.capacity
			rapid -= facility.capacity

			newS.st[facility.id] = 0
			
			newS.y[facility.id] = facility.capacity
			totalCPs -= facility.capacity
		
		elif rapid + standard >= facility.capacity:
			newS.r[facility.id] = rapid
		
			remaining = facility.capacity - rapid
			newS.st[facility.id] = remaining
			standard -= remaining
		
			newS.y[facility.id] = facility.capacity
			totalCPs -= facility.capacity
			rapid = 0

		elif rapid + standard < facility.capacity:
			newS.r[facility.id] = rapid
			newS.st[facility.id] = standard
		
			total = rapid + standard
			newS.y[facility.id] = total
			break


def closeOldFacilities(newS, openfacilityIds):
	for facilityId in openfacilityIds:
		newS.closeFacility(facilityId)

def swapFacilities(S, parameters, openFacilityIds, closedFacilityIds):
	# print("\tswapping facilities")
	newS = pickle.loads(pickle.dumps(S, -1))
	# newS = ujson.loads(ujson.dumps(S))
	# print("\t--copied")
	standard, rapid = getFacilityCPs(S, openFacilityIds)
	# print("\t--got CPs")
	openNewFacilities(newS, parameters, closedFacilityIds, standard, rapid)
	# print("\t--open new facilites")
	closeOldFacilities(newS, openFacilityIds)
	# print("\tswapped facilities")
	return newS

# RETURNS THE NUMBER OF STANDARD/RAPID CPs FOR THE GIVEN FACILITY IDS 
def getFacilityCPs(S, facilityIds):
	standard = 0
	rapid = 0
	for facilityId in facilityIds:
		standard += S.st[facilityId]
		rapid += S.r[facilityId]
	return standard, rapid


# RETURNS LISTS OF OPEN/CLOSED FACILITY IDS FOR A GIVEN ZONEID
def getOpenAndClosedFacilityIds(S, parameters, zoneId):
	openFacilities = []
	closedFacilities = []
	for facilityId in parameters.zonesDict[zoneId].facilities:
		openFacilities.append(facilityId) if S.is_open(facilityId) else closedFacilities.append(facilityId)
	return openFacilities, closedFacilities


# RETURNS A NEW SOLUTION BY SWAPPING AT MOST swaps OPEN/CLOSED FACILITIES FOR A GIVEN ZONE
# OTHERWISE THE SAME SOLUTION IS RETURNED
def getZoneNewSolution(S, parameters, zoneId, lambdaVal):
	foundBetterSolution = False
	openFacilities, closedFacilities = getOpenAndClosedFacilityIds(S, parameters, zoneId)
	openFacilityCombinations = combinationsUpToParameter(openFacilities, parameters.swaps)
	closedFacilityCombinations = combinationsUpToParameter(closedFacilities, parameters.swaps)
	allSwaps = list(itertools.product(openFacilityCombinations, closedFacilityCombinations))
	
	oldCost = S.getLagrangianCost(parameters, lambdaVal)
	newS = S
	count = 0
	for swap in allSwaps:
		count+=1
		swapsLen = len(allSwaps)
		# print("\tswap %d of %d swaps" %(count, swapsLen))
		if isSwapFeasible(S, parameters, swap[0], swap[1]):
			newS = swapFacilities(S, parameters, swap[0], swap[1])
			# newCost = newS.getLagrangianCost(parameters, lambdaVal)
			newCost = float("inf")
			if newCost < oldCost:
				foundBetterSolution = True
				break
	return newS, foundBetterSolution

def localSearch(S, parameters, lambdaVal):
	zonesLen = len(parameters.zonesDict.items())
	for zoneKey, _ in parameters.zonesDict.items():
		print("Checking zone %s (of total %d zones) which has %d facilities" %(zoneKey, zonesLen, len(parameters.zonesDict[zoneKey].facilities)))
		flag = True
		while flag:
			newS, foundBetterSolution = getZoneNewSolution(S, parameters, zoneKey, lambdaVal)
			if not foundBetterSolution:
				flag = False
			else:
				S = newS
	return newS
