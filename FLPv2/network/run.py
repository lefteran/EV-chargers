# LIBRARIES
# FILES
import network.nx_graph as nx_graph
import network.recharging_nodes as recharging_nodes
import network.clustering as clustering
import network.filter_trips as filtering
import network.slice_paths_from_delos as slice_paths_from_delos
# import network.travel_times as travel_times
import network.existing_charging_stations as existing_stations
import network.zoning as zoning


def run():
	graph = nx_graph.create_graph()
	# new_candidates = clustering.get_clusters(graph.nodes)
	# clustering.save_clusters(new_candidates)
	# candidates = clustering.load_candidates()
	# existing_stations.save_candidates_and_existing()

	candidates_and_existing = existing_stations.load_candidates_and_existing()

	# existing_stations.find_public_stations()

	# filtering.filter_trips(graph, new_candidates)

	# slice_paths_from_delos.slice_paths()

	# recharging_nodes.find_recharging_nodes_per_hour_dict(graph.nodes(), new_candidates)	# for each size 700,1k,2k,3k

	# travel_times.compute_travel_times(graph, candidates)										# for each size 700,1k,2k,3k

	zoning.get_zoning(graph, candidates_and_existing)