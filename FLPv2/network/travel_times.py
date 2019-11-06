# LIBRARIES
import json
# FILES
import network.vehicles_per_hour as vehicles_per_hour
import network.gt_shortest_paths as gt_shortest_paths
import settings



def compute_travel_times(graph, clusters):
	vehicles_network_locations_per_hour_dict = vehicles_per_hour.load_vehicles_network_locations_per_hour_dict()
	vehicles_travel_times_to_candidates_per_hour_dict = dict()

	gt_network = gt_shortest_paths.GraphToolNetwork()
	gt_network.create_graph_tool_network_from_gnx(graph)

	for hour in range(24):
		print(f'Checking hour {hour}')
		vehicles_travel_times_to_candidates_dict = gt_network.get_vehicles_travel_times_to_candidates_dict(clusters.keys(), vehicles_network_locations_per_hour_dict[str(hour)])
		vehicles_travel_times_to_candidates_per_hour_dict[str(hour)] = vehicles_travel_times_to_candidates_dict
	save_vehicles_travel_times_to_candidates_dict(vehicles_travel_times_to_candidates_per_hour_dict)



def save_vehicles_travel_times_to_candidates_dict(dict_to_be_saved):
	filename = settings.vehicles_travel_times_to_candidates
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()