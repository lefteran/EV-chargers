import time
import settings
import importData as impdt
import GraphToolNetwork as gtn
import serializationIO
import clustering
import cluster
import generateData
import sys

if __name__ == "__main__":
	start_time = time.time()
	settings.init()

	Gnx = impdt.importNetwork()
	GtNetwork = gtn.GraphToolNetwork()
	GtNetwork.createGraphToolNetworkFromGnx(Gnx)

	print("Clustering nodes ...")
	clustersFile = 'scenariosData/clustering_' + str(settings.parameters.radius) + '.json'
	settings.parameters.candidateLocations = clustering.nodeClustering(Gnx)
	theCluster = cluster.Cluster(settings.parameters.candidateLocations, (time.time() - start_time), settings.parameters.radius)
	if theCluster.hasDuplicates():
		sys.stderr.write("There are duplicates in the candidate locations list")
		sys.exit()
	serializationIO.serializeAndExport(theCluster, clustersFile)

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

