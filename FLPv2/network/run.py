# LIBRARIES
# FILES
import settings
import network.create_graph as create_graph
import network.vehicles_per_hour as vehicles_per_hour
import network.clustering as clustering
import network.all_pairs_shortest_paths as all_pairs_shortest_paths

def run():
	graph = create_graph.create_graph()
	clusters = clustering.get_clusters(graph.nodes)
	vehicles_network_locations_per_hour_dict = vehicles_per_hour.get_vehicles_network_locations_per_hour_dict(clusters, graph.nodes())
	gt_network = all_pairs_shortest_paths.GraphToolNetwork()
	gt_network.create_graph_tool_network_from_gnx(graph)
	for hour in range(24):
		vehicles_candidates_distances_dict = gt_network.get_vehicles_candidates_distances_dict(clusters.keys(), vehicles_network_locations_per_hour_dict[hour])
	a=2
