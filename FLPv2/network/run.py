# LIBRARIES
# FILES
import network.nx_graph as nx_graph
import network.vehicles_per_hour as vehicles_per_hour
import network.clustering as clustering
import network.filter_trips as filtering
# import network.travel_times as travel_times
import network.existing_charging_stations as existing_stations


def run():
	graph = nx_graph.create_graph()
	# clusters = clustering.get_clusters(graph.nodes)
	# clustering.save_clusters(clusters)
	clusters = clustering.load_clusters()

	existing_stations.find_public_stations()

	# filtering.filter_trips(graph, clusters)

	# vehicles_per_hour.get_and_save_vehicles_network_locations(graph.nodes(), clusters)	# for each size 700,1k,2k,3k

	# travel_times.compute_travel_times(graph, clusters)										# for each size 700,1k,2k,3k
