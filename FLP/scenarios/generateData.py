import settings
from random import choice, uniform
import vehicle as vh
import tripTimes


def generateVehicles(Gnx):
	edges = list(Gnx.edges())
	for i in range(settings.parameters.numberOfVehicles):
		vehicleId = i + 1
		edge = choice(edges)
		(startNode, endNode) = edge
		rn = uniform(0, 1)
		vehicle = vh.Vehicle(vehicleId, startNode, endNode, rn)
		settings.parameters.vehiclesDict[vehicleId] = vehicle


def getTimes(Gnx, GtNetwork):
	if not settings.flags.useGraphTool:
		timesDict = tripTimes.getTimeDictNx(Gnx)
	else:
		if settings.flags.parallelComputationOfTimes:
			timesDict = tripTimes.getTimeDictGtParallel(GtNetwork)
		else:
			timesDict = tripTimes.getTimeDictGt(GtNetwork)
	settings.parameters.timesDict = timesDict