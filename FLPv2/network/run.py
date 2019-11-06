# LIBRARIES
# FILES
import network.nx_graph as nx_graph
import network.vehicles_per_hour as vehicles_per_hour
import network.clustering as clustering
import network.filter_trips as filtering
import network.travel_times as travel_times

def run():
	graph = nx_graph.create_graph()
	clusters = clustering.load_clusters()

	# filtering.filter_trips(graph, clusters)

	# vehicles_per_hour.get_and_save_vehicles_network_locations(graph.nodes(), clusters)

	travel_times.compute_travel_times(graph, clusters)
