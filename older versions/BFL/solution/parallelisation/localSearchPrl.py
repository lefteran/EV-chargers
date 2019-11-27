import solution.parallelisation.splitSolutionToParts as splitToParts
from multiprocessing import Process, Lock, Manager
from math import floor
from itertools import combinations, product
from os import cpu_count, getpid
import solution.parallelisation.solutionPrl as slPrl
import _pickle as pickle
import solution.parallelisation.combinePartsIntoSolution as combineParts


def getCombinationsOfExactSwapsPrl(listOfItems, numberOfSwaps):
	combs = []
	for subset in combinations(listOfItems, numberOfSwaps):
		combs.append(list(subset))
	return combs

def isCostFinitePrl(parameters, facilityIds):
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

def getLandCostsOfNewFacilitiesPrl(parameters, newlyOpenedFacilityIds):
	landCostToAdd = 0
	for facilityId in newlyOpenedFacilityIds:
		landCostToAdd += parameters.facilitiesDict[facilityId].cost
	return landCostToAdd

def getLandCostsOfOldFacilitiesPrl(parameters, closedFacilityIds):
	landCostToSubtract = 0
	for facilityId in closedFacilityIds:
		landCostToSubtract += parameters.facilitiesDict[facilityId].cost
	return landCostToSubtract




def openNewFacilitiesPrl(newLocalPart, parameters, closedFacilityIds, standard, rapid):
	newlyOpenedFacilityIds = []
	totalCPs = standard + rapid
	L = []
	for facilityId in closedFacilityIds:
		L.append(parameters.facilitiesDict[facilityId])
	L.sort(key=lambda x: x.capacity, reverse=True)
	for facility in L:
		newLocalPart.openFacilityPrl(facility.id)
		newlyOpenedFacilityIds.append(facility.id)

		if rapid >= facility.capacity:

			newLocalPart.r[facility.id] = facility.capacity
			rapid -= facility.capacity

			newLocalPart.st[facility.id] = 0

			newLocalPart.y[facility.id] = facility.capacity
			totalCPs -= facility.capacity

		elif rapid + standard >= facility.capacity:
			newLocalPart.r[facility.id] = rapid

			remaining = facility.capacity - rapid
			newLocalPart.st[facility.id] = remaining
			standard -= remaining

			newLocalPart.y[facility.id] = facility.capacity
			totalCPs -= facility.capacity
			rapid = 0

		else:  # rapid + standard < facility.capacity
			newLocalPart.r[facility.id] = rapid
			newLocalPart.st[facility.id] = standard

			total = rapid + standard
			newLocalPart.y[facility.id] = total
			break
	return newlyOpenedFacilityIds

def closeFacilitiesPrl(localPart, openfacilityIds):
	for facilityId in openfacilityIds:
		localPart.closeFacilityPrl(facilityId)

def isSwapFeasiblePrl(localPartsDict, zoneId, parameters, openFacilityIds, closedFacilityIds):
	openCPs = 0
	closedTotalCap = 0
	for facilityId in openFacilityIds:
		openCPs += localPartsDict[zoneId].y[facilityId]
	for facilityId in closedFacilityIds:
		closedTotalCap += parameters.facilitiesDict[facilityId].capacity
	if closedTotalCap < openCPs:
		return False
	else:
		return True

def getFacilityCPsPrl(newLocalPart, facilityIds):
	standard = 0
	rapid = 0
	for facilityId in facilityIds:
		standard += newLocalPart.st[facilityId]
		rapid += newLocalPart.r[facilityId]
	return standard, rapid

def getZoneOpenAndClosedFacilityIdsPrl(localPartsDict, parameters, zoneId):
	openFacilities = []
	closedFacilities = []
	for facilityId in parameters.zonesDict[zoneId].facilities:
		openFacilities.append(facilityId) if localPartsDict[zoneId].is_openPrl(facilityId) else closedFacilities.append(facilityId)
	return openFacilities, closedFacilities

def getNewConnectivityCostPrl(globalPart, newLocalPart, localPartsDict, zoneId, parameters, openFacilityIds):
	connectivityNewCost = 0
	for openFacilityId in openFacilityIds:
		connectivityNewCost += globalPart.connectVehiclesToNewFacilityPrl(newLocalPart, localPartsDict, zoneId, parameters, openFacilityId)
	return connectivityNewCost


def swapFacilitiesPrl(globalPart, localPartsDict, zoneId, parameters, openFacilityIds, closedFacilityIds, lambdaVal, lock):
	newLocalPart = pickle.loads(pickle.dumps(localPartsDict[zoneId], -1))
	tempGlobalPart = slPrl.tempGlobalPartMapping()
	tempGlobalPart.setDict(globalPart)
	standard, rapid = getFacilityCPsPrl(newLocalPart, openFacilityIds)
	newlyOpenedFacilityIds = openNewFacilitiesPrl(newLocalPart, parameters, closedFacilityIds, standard, rapid)
	landAddedCost = getLandCostsOfNewFacilitiesPrl(parameters, newlyOpenedFacilityIds)

	############## LOCK ##############
	lock.acquire()

	connectivityNewCost = getNewConnectivityCostPrl(tempGlobalPart, newLocalPart, localPartsDict, zoneId, parameters, openFacilityIds)
	closeFacilitiesPrl(newLocalPart, openFacilityIds)
	landSubtractedCost = getLandCostsOfOldFacilitiesPrl(parameters, openFacilityIds)

	changeInCost = connectivityNewCost + lambdaVal * (landAddedCost - landSubtractedCost)
	return newLocalPart, tempGlobalPart, changeInCost


def getZoneNewSolutionPrl(globalPart, localPartsDict, parameters, zoneId, lambdaVal, lock):
	foundBetterSolution = False
	openFacilities, closedFacilities = getZoneOpenAndClosedFacilityIdsPrl(localPartsDict, parameters, zoneId)
	openFacilityCombinations = getCombinationsOfExactSwapsPrl(openFacilities, parameters.swaps)
	closedFacilityCombinations = getCombinationsOfExactSwapsPrl(closedFacilities, parameters.swaps)
	allSwaps = list(product(openFacilityCombinations, closedFacilityCombinations))
	count = 0
	swapsLen = len(allSwaps)
	for swap in allSwaps:
		count += 1
		openFacilityIds = swap[0]
		closedFacilityIds = swap[1]
		if isSwapFeasiblePrl(localPartsDict, zoneId, parameters, openFacilityIds, closedFacilityIds):
			if isCostFinitePrl(parameters, closedFacilityIds):
				############## LOCK ##############
				newLocalPart, tempGlobalPart, changeInCost = swapFacilitiesPrl(globalPart, localPartsDict, zoneId, parameters, openFacilityIds, closedFacilityIds, lambdaVal, lock)
				print("\tSwap %d of %d is feasible. The change in cost is %f" %(count, swapsLen, changeInCost))
				if changeInCost < 0:
					localPartsDict[zoneId].setNewValues(parameters, newLocalPart, zoneId)
					setGlobalPartValues(globalPart, tempGlobalPart, parameters)
					foundBetterSolution = True
					lock.release()
					break
				else:
					lock.release()
				################ UNLOCK #################
			else:
				print("\tCost of swap %d of %d is not finite" %(count, swapsLen))
		else:
			print("\tSwap %d of %d is not feasible" %(count, swapsLen))

	return foundBetterSolution


def processLocalSearch(parameters, lambdaVal, zonesList, globalPart, localPartsDict, lock):
	count = 0
	proc_id = getpid()
	zoneListLen = len(zonesList)
	for zoneId in zonesList:
		count += 1
		numberOfZoneFacilities = len(parameters.zonesDict[zoneId].facilities)
		print(f"Checking zone {zoneId} ({count}/{zoneListLen}) which has {numberOfZoneFacilities} facilities at process {proc_id}")
		flag = True
		while flag:
			foundBetterSolution = getZoneNewSolutionPrl(globalPart, localPartsDict, parameters, zoneId, lambdaVal, lock)
			if foundBetterSolution:
				print("\t\tFound better solution")
			else:
				flag = False
		# if count == 50:
		# 	break

def setInitialGlobalPartValues(S, globalPart, parameters):
	for vehicleKey, _ in parameters.vehiclesDict.items():
		# xFacilitiesDict = {}
		# for facilityKey, _ in parameters.facilitiesDict.items():
		# 	xFacilitiesDict[facilityKey] = S.x[vehicleKey][facilityKey]
		# globalPart[vehicleKey] = xFacilitiesDict
		globalPart[vehicleKey] = S.x[vehicleKey]

def setGlobalPartValues(globalPart, tempGlobalPart, parameters):
	for vehicleKey, _ in parameters.vehiclesDict.items():
		globalPart[vehicleKey] = tempGlobalPart.getVehicleDict(vehicleKey)


def distributeZonesToProcesses(S, parameters, lambdaVal):
	print("Running parallel local search ...")
	zonesLen = len(parameters.zonesDict.items())
	count = 0
	numberOfProcesses = cpu_count()			# TO UNCOMMENT
	# numberOfProcesses = 1						# TO DELETE

	localPartsDict, globalPart = splitToParts.getSharedAndIndependentPartsOfSolution(S, parameters)
	manager = Manager()
	lock = manager.Lock()
	globalPart = manager.dict()
	setInitialGlobalPartValues(S, globalPart, parameters)

	zoneIdsList = list(parameters.zonesDict.keys())
	zoneIdsListLength = len(zoneIdsList)
	zonesPerProcess = floor(zoneIdsListLength / numberOfProcesses)
	processes = []
	first = 0
	last = zonesPerProcess + 1
	print("Starting multiprocessing ...")
	for i in range(numberOfProcesses):
		# processLocalSearch(parameters, lambdaVal, zoneIdsList, globalPart, localPartsDict, lock)
	# ******************  TO UNCOMMENT BELOW **************************************
		process = Process(target = processLocalSearch, args = (parameters, lambdaVal, zoneIdsList[first:last], globalPart, localPartsDict, lock))
		processes.append(process)
		process.start()
		first += zonesPerProcess
		last = last + zonesPerProcess if i < numberOfProcesses - 1 else zoneIdsListLength - 1
	for process in processes:
		process.join()
	S = combineParts.combinePartsIntoOneSolution(globalPart, localPartsDict, parameters)
	return S