import solution.localSolutionPart as lsl
import solution.globalSolutionPart as gsl
from multiprocessing import Process, Lock, Value
from math import floor


# def getParallelZoneNewSolution(S, parameters, zoneId, lambdaVal):
#     foundBetterSolution = False
#     openFacilities, closedFacilities = getOpenAndClosedFacilityIds(S, parameters, zoneId)
#     openFacilityCombinations = combinationsUpToParameter(openFacilities, parameters.swaps)
#     closedFacilityCombinations = combinationsUpToParameter(closedFacilities, parameters.swaps)
#     allSwaps = list(itertools.product(openFacilityCombinations, closedFacilityCombinations))
#
#     # oldCost = S.getLagrangianCost(parameters, lambdaVal)
#     newS = S
#     count = 0
#     swapsLen = len(allSwaps)
#     for swap in allSwaps:
#         count += 1
#         openFacilityIds = swap[0]
#         closedFacilityIds = swap[1]
#         if isSwapFeasible(S, parameters, openFacilityIds, closedFacilityIds):
#             if isCostFinite(parameters, closedFacilityIds):
#                 isCostFinite(parameters, closedFacilityIds)
#                 newS, changeInCost = swapFacilities(S, parameters, openFacilityIds, closedFacilityIds)
#                 # newCost = newS.getLagrangianCost(parameters, lambdaVal)
#                 print("Swap %d of %d is feasible. Oldcost is %f and the change in cost is %f" % (
#                 count, swapsLen, oldCost, changeInCost))
#                 if changeInCost > 0:
#                     foundBetterSolution = True
#                     break
#             else:
#                 print("Cost of swap %d of %d is not finite" % (count, swapsLen))
#         else:
#             print("Swap %d of %d is not feasible" % (count, swapsLen))
#     return newS, foundBetterSolution

def parallelProcessingOfZones(parameters, lambdaVal, zonesList, globalPart, localSolutionsDict):
	for zoneId in zonesList:
		flag = True
		while flag:
			newS, foundBetterSolution = getZoneNewSolution(S, parameters, zoneId, lambdaVal)
			if not foundBetterSolution:
				flag = False
			else:
				S = newS

def parallelProcessingLocalSearch(S, parameters, lambdaVal, numberOfProcesses):
	zonesLen = len(parameters.zonesDict.items())
	count=0
	localSolutionsDict = {}
	zoneIdsList = []
	for zoneKey, _ in parameters.zonesDict.items():
		localSolutionsDict[zoneKey] = lsl.localPartOfSolution(parameters, S, zoneKey)
		zoneIdsList.append(zoneKey)
	globalPart = gsl.globalPartOfSolution(parameters, S)
	zoneIdsListLength = len(zoneIdsList)
	zonesPerProcess = floor(zoneIdsListLength / numberOfProcesses)
	processes = []
	first = 0
	last = zonesPerProcess + 1
    # DEBUG THE SINGLE PROCESS LOCAL SEARCH FIRST AND THEN CHECK THE PARALLEL PROCESSING
	for i in range(numberOfProcesses):
		process = Process(target=parallelProcessingOfZones, args=(parameters, lambdaVal, zoneIdsList[first, last], globalPart, localSolutionsDict))
		processes.append(process)
		process.start()
		first += zonesPerProcess
		last = last + zonesPerProcess if i < numberOfProcesses - 1 else zoneIdsListLength - 1
	for process in processes:
		process.join()
