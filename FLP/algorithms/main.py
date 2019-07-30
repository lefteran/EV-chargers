import time
import settings
import importData as impdt
import serializationIO
import fwdGreedy
import backGreedy
import solution
import jsonpickle
import sys
import randomLocalSearch


if __name__ == "__main__":
	start_time = time.time()
	settings.init()

	Gnx = impdt.importNetwork()

	print("Getting vehicles and vehicle-facility times ...")
	impdt.getVehicles()
	impdt.getTimes()
	clusterFilename = 'clusters/clustering_' + str(settings.parameters.radius) + '.json'
	cluster = serializationIO.importAndDeserialize(clusterFilename)
	settings.parameters.candidateLocations = cluster['candidateLocations']

	algorithmDict = {1: "Forward Greedy",
					 2: "Backward Greedy",
					 3: "Random Local Search"}
	algorithm = 2

	if algorithm == 1:
		S, totalCost = fwdGreedy.forwardGreedy()
		filename = "solutions/fwdGreedy_" + str(settings.parameters.k) + '_' + str(settings.parameters.radius) + ".json"
	elif algorithm == 2:
		S, totalCost = backGreedy.backwardGreedy()
		filename = "solutions/backGreedy_" + str(settings.parameters.k) + '_' + str(settings.parameters.radius) +  ".json"
	elif algorithm == 3:
		S, totalCost = randomLocalSearch.randomLocalSearch()
		filename = "solutions/rndLocalSearch_" + str(settings.parameters.k) + '_' + str(settings.parameters.radius) +  ".json"
	else:
		sys.stderr.write("Unknown algorithm")
		sys.exit()

	solObject = solution.Solution(S, totalCost, algorithm, (time.time() - start_time))
	serializationIO.serializeAndExport(solObject, filename)

	# print(f"\nS is {S} with cost = {totalCost}")

	print("--- %s seconds ---" % (time.time() - start_time))

