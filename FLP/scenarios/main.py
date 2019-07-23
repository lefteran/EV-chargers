import time
import settings
import importData as impdt
import GraphToolNetwork as gtn
import serializationIO

if __name__ == "__main__":
	start_time = time.time()
	print("#########################################################\n#########################################################")
	settings.init()
	# print(f"setting value is {settings.parameters.gamma}")

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
	timesFile = "scenario1/timesdict.json"
	serializationIO.serializeAndExport(settings.parameters.vehiclesDict, vehiclesFile)
	serializationIO.exportDeterministicTripTimes(settings.parameters.timesDict, timesFile)

	print("--- %s seconds ---" % (time.time() - start_time))

