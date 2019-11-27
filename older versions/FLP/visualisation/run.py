import time
import settings
import visualisation.visualisation as visualisation
import i_o.importData as impdt
import i_o.serializationIO as saveLoadNetwork


def run():
	start_time = time.time()
	# settings.init()

	Gnx = impdt.importNetwork()

	place = 'chicago'
	networkName = settings.places[place]
	filename = place + '.graphml'

	settings.resetFilePaths()
	G = visualisation.visualiseNetwork(networkName, filename, place)
	if settings.saveNetwork:
		saveLoadNetwork.saveNetwork(G, filename)

	print("--- %s seconds ---" % (time.time() - start_time))


