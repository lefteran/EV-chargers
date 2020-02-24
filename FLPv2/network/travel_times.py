# LIBRARIES
import json
from math import ceil
# FILES
import network.recharging_nodes as recharging_nodes
import network.gt_shortest_paths as gt_shortest_paths
import settings


def load_vehicles_travel_times_to_candidates_dict():
	filename = settings.travel_times_per_hour
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return json_dict


def save_vehicles_travel_times_to_candidates_dict(dict_to_be_saved):
	filename = settings.travel_times_per_hour
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


# def convert_travel_times_to_seconds(vehicles_travel_times_to_candidates):
# 	vehicles_travel_times_to_candidates_in_seconds = dict()
# 	for hour in range(24):
# 		vehicles_travel_times_to_candidates_per_hour_in_seconds = dict()
# 		vehicles_travel_times_to_candidates_per_hour_dict = vehicles_travel_times_to_candidates[str(hour)]
# 		for vehicle_candidate_key, vehicle_candidate_travel_time in vehicles_travel_times_to_candidates_per_hour_dict.items():
# 			rounded_travel_time_in_seconds = ceil(vehicle_candidate_travel_time * 3600.0)
# 			vehicles_travel_times_to_candidates_per_hour_in_seconds[vehicle_candidate_key] = rounded_travel_time_in_seconds
# 		vehicles_travel_times_to_candidates_in_seconds[str(hour)] = vehicles_travel_times_to_candidates_per_hour_in_seconds
# 	return vehicles_travel_times_to_candidates_in_seconds


def convert_travel_times_to_seconds(travel_times_per_hour):
	travel_times_in_seconds = dict()
	for hour in range(24):
		travel_times_in_seconds[str(hour)] = dict()
		for vehicle in travel_times_per_hour[str(hour)].keys():
			for candidate in travel_times_per_hour[str(hour)][vehicle].keys():
				rounded_travel_time_in_seconds = ceil(travel_times_per_hour[str(hour)][vehicle][candidate] * 3600.0)
				if vehicle not in travel_times_in_seconds[str(hour)]:
					travel_times_in_seconds[str(hour)][vehicle] = dict()
				travel_times_in_seconds[str(hour)][vehicle][candidate] = rounded_travel_time_in_seconds
	return travel_times_in_seconds

	# 	vehicles_travel_times_to_candidates_per_hour_in_seconds = dict()
	# 	vehicles_travel_times_to_candidates_per_hour_dict = vehicles_travel_times_to_candidates[str(hour)]
	# 	for vehicle_candidate_key, vehicle_candidate_travel_time in vehicles_travel_times_to_candidates_per_hour_dict.items():
	# 		rounded_travel_time_in_seconds = ceil(vehicle_candidate_travel_time * 3600.0)
	# 		vehicles_travel_times_to_candidates_per_hour_in_seconds[vehicle_candidate_key] = rounded_travel_time_in_seconds
	# 	vehicles_travel_times_to_candidates_in_seconds[str(hour)] = vehicles_travel_times_to_candidates_per_hour_in_seconds
	# return vehicles_travel_times_to_candidates_in_seconds


def compute_travel_times(graph, candidates):
	recharging_nodes_per_hour_dict = recharging_nodes.load_recharging_nodes_per_hour_dict()
	vehicles_travel_times_to_candidates_per_hour_dict = dict()

	gt_network = gt_shortest_paths.GraphToolNetwork()
	gt_network.create_graph_tool_network_from_gnx(graph)

	for hour in range(24):
		print(f'Checking hour {hour}')
		vehicles_travel_times_to_candidates_dict = gt_network.get_vehicles_travel_times_to_candidates_dict(candidates, recharging_nodes_per_hour_dict[str(hour)])
		vehicles_travel_times_to_candidates_per_hour_dict[str(hour)] = vehicles_travel_times_to_candidates_dict
	vehicles_travel_times_to_candidates_in_seconds = convert_travel_times_to_seconds(vehicles_travel_times_to_candidates_per_hour_dict)
	save_vehicles_travel_times_to_candidates_dict(vehicles_travel_times_to_candidates_in_seconds)


