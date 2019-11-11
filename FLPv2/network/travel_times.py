# LIBRARIES
import json
from math import ceil
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
	vehicles_travel_times_to_candidates_in_seconds = convert_travel_times_to_seconds(vehicles_travel_times_to_candidates_per_hour_dict)
	save_vehicles_travel_times_to_candidates_dict(vehicles_travel_times_to_candidates_in_seconds)


def convert_travel_times_to_seconds(vehicles_travel_times_to_candidates):
	vehicles_travel_times_to_candidates_in_seconds = dict()
	for hour in range(24):
		vehicles_travel_times_to_candidates_per_hour_in_seconds = dict()
		vehicles_travel_times_to_candidates_per_hour_dict = vehicles_travel_times_to_candidates[str(hour)]
		for vehicle_candidate_key, vehicle_candidate_travel_time in vehicles_travel_times_to_candidates_per_hour_dict.items():
			rounded_travel_time_in_seconds = ceil(vehicle_candidate_travel_time * 3600.0)
			vehicles_travel_times_to_candidates_per_hour_in_seconds[
				vehicle_candidate_key] = rounded_travel_time_in_seconds
		vehicles_travel_times_to_candidates_in_seconds[
			str(hour)] = vehicles_travel_times_to_candidates_per_hour_in_seconds
	return vehicles_travel_times_to_candidates_in_seconds


def load_vehicles_travel_times_to_candidates_dict():
	filename = settings.vehicles_travel_times_to_candidates
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return json_dict



def save_vehicles_travel_times_to_candidates_dict(dict_to_be_saved):
	filename = settings.vehicles_travel_times_to_candidates
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()