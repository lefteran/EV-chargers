# LIBRARIES
import time
import GraphToolNetwork as gtn
import sys
import os
# FILES
import settings
import i_o.importData as impdt
import i_o.serializationIO as serializationIO
import scenarios.clustering as clustering
import scenarios.cluster as cluster
import scenarios.generateData as generateData

def run():
	start_time = time.time()
	settings.init()

	# TODO: Check if the current interpreter is Docker
	Gnx = impdt.importNetwork()
	GtNetwork = gtn.GraphToolNetwork()
	GtNetwork.createGraphToolNetworkFromGnx(Gnx)

	print("Clustering nodes ...")
	if not os.path.isdir(settings.scenarioDirectory):
		os.mkdir(settings.scenarioDirectory)
	if os.path.isfile(settings.clustersFile):
		cluster = serializationIO.importAndDeserialize(settings.clustersFile)
		settings.candidateLocations = cluster.candidateLocations
	else:
		settings.candidateLocations = clustering.nodeClustering(Gnx)
		theCluster = cluster.Cluster(settings.candidateLocations, (time.time() - start_time), settings.radius)
		if theCluster.hasDuplicates():
			sys.stderr.write("There are duplicates in the candidate locations list")
			sys.exit()
		serializationIO.serializeAndExport(theCluster, settings.clustersFile)



	print("Generating vehicles' locations ...")
	generateData.generateVehicles(Gnx)
	serializationIO.serializeAndExport(settings.vehiclesDict, settings.vehiclesDictFile)

	print("Computing vehicle-facility times ...")
	generateData.getTimes(Gnx, GtNetwork)
	timesFile = 'scenariosData/timesDict_' + str(settings.numberOfVehicles) + '_' + str(settings.radius) + '.csv'
	serializationIO.exportDeterministicTripTimes(settings.timesDict, timesFile)

	print("--- %s seconds ---" % (time.time() - start_time))

