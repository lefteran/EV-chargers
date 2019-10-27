# LIBRARIES
# FILES
import network.create_graph as create_graph
import network.vehicles_per_hour as vehicles_per_hour
import network.clustering as clustering
import network.shortest_paths as shortest_paths
import network.gt_shortest_paths as gt_shortest_paths

def run():
	graph = create_graph.create_graph()
	clusters = clustering.load_clusters()
	# clusters = clustering.get_clusters(graph.nodes)
	# clustering.save_clusters(clusters)
	vehicles_network_locations_per_hour_dict = vehicles_per_hour.get_vehicles_network_locations_per_hour_dict(clusters, graph.nodes())
	# vehicles_per_hour.save_vehicles_network_locations_per_hour_dict(vehicles_network_locations_per_hour_dict)


	# vehicles_distances_to_candidates_per_hour_dict = dict()
	vehicles_travel_times_to_candidates_per_hour_dict = dict()

	gt_network = gt_shortest_paths.GraphToolNetwork()
	gt_network.create_graph_tool_network_from_gnx(graph)

	for hour in range(24):
		print(f'Checking hour {hour}')
		# vehicles_distances_to_candidates_dict = shortest_paths.get_vehicles_distances_to_candidates_dict(graph, clusters.keys(), vehicles_network_locations_per_hour_dict[str(hour)])
		vehicles_travel_times_to_candidates_dict = gt_network.get_vehicles_travel_times_to_candidates_dict(clusters.keys(), vehicles_network_locations_per_hour_dict[str(hour)])
		# vehicles_distances_to_candidates_per_hour_dict[str(hour)] = vehicles_distances_to_candidates_dict
		vehicles_travel_times_to_candidates_per_hour_dict[str(hour)] = vehicles_travel_times_to_candidates_dict
	# shortest_paths.save_vehicles_distances_to_candidates_dict(vehicles_distances_to_candidates_per_hour_dict)
	shortest_paths.save_vehicles_travel_times_to_candidates_dict(vehicles_travel_times_to_candidates_per_hour_dict)


