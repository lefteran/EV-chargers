import solution.parallelisation.solutionPrl as slPrl

def getSharedAndIndependentPartsOfSolution(S, parameters):
	localPartsDict = {}
	for zoneKey, _ in parameters.zonesDict.items():
		localPartsDict[zoneKey] = slPrl.localPartOfSolution(parameters, S, zoneKey)
	globalPart = slPrl.globalPartOfSolution(parameters, S)
	return localPartsDict, globalPart
