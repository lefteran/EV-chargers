# LIBRARIES
import time
from sys import stderr, exit
import os
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
	# numberOfVehiclesList = [30, 60, 100, 200, 500, 1000]
	numberOfVehiclesList = [30]

	for numberOfVehicles in numberOfVehiclesList:
		settings.numberOfVehicles = numberOfVehicles
		settings.resetFilePaths()

		print("Getting vehicles and vehicle-facility times ...")
		impdt.getVehicles()
		impdt.getTimes()
		cluster = serializationIO.importAndDeserialize(settings.clusterFilename)
		settings.candidateLocations = cluster['candidateLocations']

		S, totalCost, filename = None, None, None
		if settings.algorithm == 1:
			S, totalCost = fwdGreedy.forwardGreedy()
			if not os.path.isdir(settings.fwdGreedykDir):
				os.mkdir(settings.fwdGreedykDir)
			filename = settings.fwdGreedyFile

		elif settings.algorithm == 2:
			S, totalCost = backGreedy.backwardGreedy()
			if not os.path.isdir(settings.backGreedykDir):
				os.mkdir(settings.backGreedykDir)
			filename = settings.backGreedyFile

		elif settings.algorithm == 3:
			S, totalCost = randomLocalSearch.randomLocalSearch()
			if not os.path.isdir(settings.randomLocalSearchkDir):
				os.mkdir(settings.randomLocalSearchkDir)
			filename = settings.randomLocalSearchFile

		else:
			stderr.write("Unknown algorithm")
			exit()

		solObject = solution.Solution(S, totalCost, settings.algorithm, (time.time() - start_time))
		serializationIO.serializeAndExport(solObject, filename)

	# print(f"\nS is {S} with cost = {totalCost}")

