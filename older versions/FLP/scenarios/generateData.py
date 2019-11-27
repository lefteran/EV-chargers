# LIBRARIES
from random import choice, uniform
# FILES
import settings
import agents.vehicle as vh
import scenarios.tripTimes as tripTimes


def generateVehicles(Gnx):
	edges = list(Gnx.edges())
	for i in range(settings.numberOfVehicles):
		vehicleId = i + 1
		edge = choice(edges)
		(startNode, endNode) = edge
		rn = uniform(0, 1)
		vehicle = vh.Vehicle(vehicleId, startNode, endNode, rn)
		settings.vehiclesDict[vehicleId] = vehicle


def getTimes(Gnx, GtNetwork):
	if not settings.useGraphTool:
		timesDict = tripTimes.getTimeDictNx(Gnx)
	else:
		if settings.parallelComputationOfTimes:
			timesDict = tripTimes.getTimeDictGtParallel(GtNetwork)
		else:
			timesDict = tripTimes.getTimeDictGt(GtNetwork)
	settings.timesDict = timesDict