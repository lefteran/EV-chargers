import solution.parallelisation.localSolutionPart as lsl
import solution.parallelisation.globalSolutionPart as gsl


def getSolutionSharedAndIndependentParts(S, parameters):
	localPartsDict = {}
	for zoneKey, _ in parameters.zonesDict.items():
		localPartsDict[zoneKey] = lsl.localPartOfSolution(parameters, S, zoneKey)
	globalPart = gsl.globalPartOfSolution(parameters, S)
	return localPartsDict, globalPart
