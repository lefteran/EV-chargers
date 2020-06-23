# LIBRARIES
# FILES
import settings
import network.nx_graph as nx_graph
import network.recharging_nodes as recharging_nodes
import network.clustering as clustering
import network.filter_trips as filtering
import network.slice_paths_from_delos as slice_paths_from_delos
import network.travel_times as travel_times
import network.existing_charging_stations as existing_stations
import network.zoning as zoning
import network.traffic_demand as traffic_demand

def run():
	graph = nx_graph.create_graph()
	# new_candidates = clustering.get_clusters(graph.nodes)
	# clustering.save_clusters(new_candidates)
	candidates = clustering.load_candidates()
	# existing_stations.get_existing_stations(graph.nodes())

	existing_stations_dict = existing_stations.load_json(settings.existing_stations)

	# candidates_and_existing = existing_stations.load_json(settings.candidates_and_existing)

	# filtering.filter_trips(graph, new_candidates)

	# slice_paths_from_delos.slice_paths()
	# 
	# # recharging_nodes.find_recharging_nodes_per_hour_dict(graph.nodes(), candidates)	# for each size 700,1k,2k,3k
	# 
	# recharging_nodes.find_recharging_nodes_list(graph.nodes(), candidates, list(existing_stations_dict.keys()))
	# 
	# recharging_nodes.find_recharging_nodes_duplicates()

	travel_times.compute_travel_times(graph, candidates, list(existing_stations_dict.keys()))										# for each size 700,1k,2k,3k

	# zoning.candidate_zoning(graph, list(candidates.keys()))

	# zoning.existing_zoning(graph, list(existing_stations_dict.keys()))

	# traffic_demand.compute_traffic_demand(graph)
