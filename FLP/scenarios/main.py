import time
import settings
import importData as impdt
import GraphToolNetwork as gtn
import serializationIO

if __name__ == "__main__":
	start_time = time.time()
	settings.init()

	Gnx = impdt.importNetwork()
	if settings.flags.importTimes:
		GtNetwork = None
	else:
		GtNetwork = gtn.GraphToolNetwork()
		GtNetwork.createGraphToolNetworkFromGnx(Gnx)

	print("Getting vehicles and vehicle-facility times ...")
	impdt.getVehicles(Gnx)
	impdt.getTimes(Gnx, GtNetwork)

	vehiclesFile = "scenario1/vehiclesDict.json"
	timesFile = "scenario1/timesDict.csv"
	serializationIO.serializeAndExport(settings.parameters.vehiclesDict, vehiclesFile)
	serializationIO.exportDeterministicTripTimes(settings.parameters.timesDict, timesFile)

	print("--- %s seconds ---" % (time.time() - start_time))

