# LIBRARIES
import json
from math import ceil
# FILES
import network.recharging_nodes as recharging_nodes
import network.gt_shortest_paths as gt_shortest_paths
import settings


def load_json(filename):
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return json_dict


def save_travel_times_to_candidates_dict(dict_to_be_saved, filename):
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


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


def convert_traffic_travel_times_to_seconds(traffic_travel_times):
	for vehicle in traffic_travel_times.keys():
		for candidate in traffic_travel_times[vehicle].keys():
			traffic_travel_times[vehicle][candidate] = ceil(traffic_travel_times[vehicle][candidate] * 3600.0)


def compute_fleet_travel_times(graph, candidates):
	recharging_nodes_per_hour_dict = load_json(settings.recharging_nodes_per_hour)
	vehicles_travel_times_to_candidates_per_hour_dict = dict()

	gt_network = gt_shortest_paths.GraphToolNetwork()
	gt_network.create_graph_tool_network_from_gnx(graph)

	for hour in range(24):
		print(f'Checking hour {hour}')
		vehicles_travel_times_to_candidates_dict = gt_network.get_travel_times_to_candidates_dict(candidates, recharging_nodes_per_hour_dict[str(hour)])
		vehicles_travel_times_to_candidates_per_hour_dict[str(hour)] = vehicles_travel_times_to_candidates_dict
	vehicles_travel_times_to_candidates_in_seconds = convert_travel_times_to_seconds(vehicles_travel_times_to_candidates_per_hour_dict)
	save_travel_times_to_candidates_dict(vehicles_travel_times_to_candidates_in_seconds, settings.travel_times_per_hour)


def compute_traffic_travel_times(graph, candidates):
	traffic_dict = load_json(settings.traffic_demand)
	traffic_nodes = [int(i) for i in list(traffic_dict.keys())]

	gt_network = gt_shortest_paths.GraphToolNetwork()
	gt_network.create_graph_tool_network_from_gnx(graph)

	traffic_travel_times_dict = gt_network.get_travel_times_to_candidates_dict(candidates, traffic_nodes)
	convert_traffic_travel_times_to_seconds(traffic_travel_times_dict)
	save_travel_times_to_candidates_dict(traffic_travel_times_dict, settings.traffic_travel_times)


def compute_travel_times(graph, candidates):
	compute_fleet_travel_times(graph, candidates)
	compute_traffic_travel_times(graph, candidates)


