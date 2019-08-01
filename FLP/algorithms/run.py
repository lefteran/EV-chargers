# LIBRARIES
import time
from sys import stderr, exit
# FILES
import settings
import i_o.importData as impdt
import i_o.serializationIO as serializationIO
import algorithms.fwdGreedy as fwdGreedy
import algorithms.backGreedy as backGreedy
import algorithms.solution as solution
import algorithms.randomLocalSearch as randomLocalSearch


def run():
	start_time = time.time()
	Gnx = impdt.importNetwork()

	print("Getting vehicles and vehicle-facility times ...")
	impdt.getVehicles()
	impdt.getTimes()
	cluster = serializationIO.importAndDeserialize(settings.filePaths.clusterFilename)
	settings.parameters.candidateLocations = cluster['candidateLocations']


	S, totalCost, filename = None, None, None
	if settings.parameters.algorithm == 1:
		S, totalCost = fwdGreedy.forwardGreedy()
		filename = settings.filePaths.fwdGreedyFile
	elif settings.parameters.algorithm == 2:
		S, totalCost = backGreedy.backwardGreedy()
		filename = settings.filePaths.backGreedyFile
	elif settings.parameters.algorithm == 3:
		S, totalCost = randomLocalSearch.randomLocalSearch()
		filename = settings.filePaths.randomLocalSearchFile
	else:
		stderr.write("Unknown algorithm")
		exit()

	solObject = solution.Solution(S, totalCost, settings.parameters.algorithm, (time.time() - start_time))
	serializationIO.serializeAndExport(solObject, filename)

	# print(f"\nS is {S} with cost = {totalCost}")

