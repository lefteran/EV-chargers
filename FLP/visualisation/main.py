import time
import settings
import visualisation
import importData as impdt
import saveLoadNetwork


if __name__ == "__main__":
	start_time = time.time()
	settings.init()

	Gnx = impdt.importNetwork()

	# networkName = 'Piedmont, California'
	networkName = 'Chicago, Cook County, Illinois, USA'

	G = visualisation.visualiseNetwork(networkName)
	if settings.flags.saveNetwork:
		saveLoadNetwork.saveNetwork(G, 'Chicago.graphml')

	print("--- %s seconds ---" % (time.time() - start_time))


