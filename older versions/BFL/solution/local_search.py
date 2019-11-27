import itertools
import _pickle as pickle


def getCombinationsUpToParameter(L, p):
	combs = []
	for i in range(p):
		for subset in itertools.combinations(L, i+1):
			combs.append(list(subset))
	return combs

def getCombinationsOfExactSwaps(listOfItems, numberOfSwaps):
	combs = []
	for subset in itertools.combinations(listOfItems, numberOfSwaps):
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
	newlyOpenedFacilityIds = []
	totalCPs = standard + rapid
	L = []
	for facilityId in closedFacilityIds:
		L.append(parameters.facilitiesDict[facilityId])
	L.sort(key=lambda x: x.capacity, reverse=True)
	for facility in L:
		newS.openFacility(facility.id)
		newlyOpenedFacilityIds.append(facility.id)

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

		else: #rapid + standard < facility.capacity
			newS.r[facility.id] = rapid
			newS.st[facility.id] = standard
		
			total = rapid + standard
			newS.y[facility.id] = total
			break
	return newlyOpenedFacilityIds

def closeFacilities(newS, openfacilityIds):
	for facilityId in openfacilityIds:
		newS.closeFacility(facilityId)

def getLandCostsOfOldFacilities(parameters, closedFacilityIds):
	landCostToSubtract = 0
	for facilityId in closedFacilityIds:
		landCostToSubtract += parameters.facilitiesDict[facilityId].cost
	return landCostToSubtract


def getLandCostsOfNewFacilities(parameters, newlyOpenedFacilityIds):
	landCostToAdd = 0
	for facilityId in newlyOpenedFacilityIds:
		landCostToAdd += parameters.facilitiesDict[facilityId].cost
	return landCostToAdd

def getNewConnectivityCost(S, parameters, openFacilityIds):
	connectivityNewCost = 0
	for openFacilityId in openFacilityIds:
		connectivityNewCost += S.connectVehiclesToNewFacility(parameters, openFacilityId)
	return connectivityNewCost

def swapFacilities(S, parameters, openFacilityIds, closedFacilityIds, lambdaVal):
	newS = pickle.loads(pickle.dumps(S, -1))
	standard, rapid = getFacilityCPs(S, openFacilityIds)

	newlyOpenedFacilityIds = openNewFacilities(newS, parameters, closedFacilityIds, standard, rapid)
	landAddedCost = getLandCostsOfNewFacilities(parameters, newlyOpenedFacilityIds)
	connectivityNewCost = getNewConnectivityCost(newS, parameters, openFacilityIds)
	closeFacilities(newS, openFacilityIds)
	landSubtractedCost = getLandCostsOfOldFacilities(parameters, openFacilityIds)

	changeInCost = connectivityNewCost + lambdaVal * (landAddedCost - landSubtractedCost)
	return newS, changeInCost

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

def isCostFinite(parameters, facilityIds):
	isFinite = False
	for vehicleKey,_ in parameters.vehiclesDict.items():
		isFinite = False
		for facilityId in facilityIds:
			if parameters.timesDict[vehicleKey][facilityId] != float("inf"):
				isFinite = True
				break
		if not isFinite:
			return isFinite
	return isFinite


# RETURNS A NEW SOLUTION BY SWAPPING AT MOST swaps OPEN/CLOSED FACILITIES FOR A GIVEN ZONE
# OTHERWISE THE SAME SOLUTION IS RETURNED
def getZoneNewSolution(S, parameters, zoneId, lambdaVal):
	foundBetterSolution = False
	openFacilities, closedFacilities = getOpenAndClosedFacilityIds(S, parameters, zoneId)
	openFacilityCombinations = getCombinationsOfExactSwaps(openFacilities, parameters.swaps)
	closedFacilityCombinations = getCombinationsOfExactSwaps(closedFacilities, parameters.swaps)
	allSwaps = list(itertools.product(openFacilityCombinations, closedFacilityCombinations))
	# oldCost = S.getLagrangianCost(parameters, lambdaVal)
	newS = None
	count = 0
	swapsLen = len(allSwaps)
	for swap in allSwaps:
		count += 1
		openFacilityIds = swap[0]
		closedFacilityIds = swap[1]
		if isSwapFeasible(S, parameters, openFacilityIds, closedFacilityIds):
			if isCostFinite(parameters, closedFacilityIds):
				# isCostFinite(parameters, closedFacilityIds)
				newS, changeInCost = swapFacilities(S, parameters, openFacilityIds, closedFacilityIds, lambdaVal)
				# newCost = newS.getLagrangianCost(parameters, lambdaVal)
				print("\tSwap %d of %d is feasible. The change in cost is %f" %(count, swapsLen, changeInCost))
				if changeInCost < 0:
					foundBetterSolution = True
					break
			else:
				print("\tCost of swap %d of %d is not finite" %(count, swapsLen))
		else:
			print("\tSwap %d of %d is not feasible" %(count, swapsLen))
	return newS, foundBetterSolution


def localSearch(S, parameters, lambdaVal):
	print("Running local search ...")
	zonesLen = len(parameters.zonesDict.items())
	count = 0
	newS = None
	for zoneKey, _ in parameters.zonesDict.items():
		count += 1
		numberOfZoneFacilities = len(parameters.zonesDict[zoneKey].facilities)
		print(f"Checking zone {count} (of total {zonesLen} zones) which has {numberOfZoneFacilities} facilities")
		# if len(parameters.zonesDict[zoneKey].facilities) >= 100:
		# 	a=2
		# print("Current solution cost is %f" %(S.getLagrangianCost(parameters, lambdaVal)))
		flag = True
		while flag:
			newS, foundBetterSolution = getZoneNewSolution(S, parameters, zoneKey, lambdaVal)
			if foundBetterSolution:
				print("\t\tFound better solution")
				S = newS
				newCost = S.getCost(parameters)
			else:
				flag = False
	return S
