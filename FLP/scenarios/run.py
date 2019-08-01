# LIBRARIES
import time
import GraphToolNetwork as gtn
import sys
# FILES
import settings
import importData as impdt
import serializationIO
import clustering
import cluster
import generateData

def run():
	start_time = time.time()
	settings.init()

	# TODO: Check if the current interpreter is Docker
	Gnx = impdt.importNetwork()
	GtNetwork = gtn.GraphToolNetwork()
	GtNetwork.createGraphToolNetworkFromGnx(Gnx)

	print("Clustering nodes ...")
	settings.parameters.candidateLocations = clustering.nodeClustering(Gnx)
	theCluster = cluster.Cluster(settings.parameters.candidateLocations, (time.time() - start_time), settings.parameters.radius)
	if theCluster.hasDuplicates():
		sys.stderr.write("There are duplicates in the candidate locations list")
		sys.exit()
	serializationIO.serializeAndExport(theCluster, settings.filePaths.clustersFile)

	# cluster = serializationIO.importAndDeserialize(clustersFile)
	# settings.parameters.candidateLocations = cluster.candidateLocations


	print("Generating vehicles' locations ...")
	# impdt.getVehicles(Gnx)
	generateData.generateVehicles(Gnx)
	vehiclesFile = 'scenariosData/vehiclesDict_' + str(settings.parameters.numberOfVehicles) + '.json'
	serializationIO.serializeAndExport(settings.parameters.vehiclesDict, vehiclesFile)

	print("Computing vehicle-facility times ...")
	generateData.getTimes(Gnx, GtNetwork)
	timesFile = 'scenariosData/timesDict_' + str(settings.parameters.numberOfVehicles) + '_' + str(settings.parameters.radius) + '.csv'
	serializationIO.exportDeterministicTripTimes(settings.parameters.timesDict, timesFile)

	print("--- %s seconds ---" % (time.time() - start_time))

