# LIBRARIES
import time
# FILES
import settings
import network.nx_graph as nx_graph
import visualisation.visualisation as visualisation
import visualisation.node_heatmap as heatmap


def run():
	start_time = time.time()

	# place = 'chicago'
	#
	# visualisation.visualise_network(place)

	print("--- %s seconds ---" % (time.time() - start_time))


