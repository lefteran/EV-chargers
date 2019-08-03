import time
import settings
import visualisation
import importData as impdt
import saveLoadNetwork


if __name__ == "__main__":
	start_time = time.time()
	settings.init()

	Gnx = impdt.importNetwork()

	place = 'chicago'
	networkName = settings.places[place]
	filename = place + '.graphml'

	G = visualisation.visualiseNetwork(networkName, filename, place)
	if settings.saveNetwork:
		saveLoadNetwork.saveNetwork(G, filename)

	print("--- %s seconds ---" % (time.time() - start_time))


