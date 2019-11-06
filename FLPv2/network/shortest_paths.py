# LIBRARIES
import networkx as nx
import json
# FILES
import settings

def get_vehicles_distances_to_candidates_dict(graph, candidate_nodes, vehicles_nodes):
	from tqdm import tqdm
	vehicles_distances_to_candidates_dict = dict()
	for source_node in tqdm(vehicles_nodes):
		for target_node in candidate_nodes:
			distance = nx.shortest_path_length(graph, source=source_node, target=int(target_node), weight='length')
			vehicles_distances_to_candidates_dict[str(source_node) + '-' + str(target_node)] = distance
	return vehicles_distances_to_candidates_dict


def get_vehicles_travel_times_to_candidates_dict(graph, candidate_nodes, vehicles_nodes):
	vehicles_travel_times_to_candidates_dict = dict()
	for source_node in vehicles_nodes:
		for target_node in candidate_nodes:
			travel_time = nx.shortest_path_length(graph, source=source_node, target=int(target_node), weight='traveltime')
			vehicles_travel_times_to_candidates_dict[str(source_node) + '-' + str(target_node)] = travel_time
	return vehicles_travel_times_to_candidates_dict


def save_vehicles_distances_to_candidates_dict(dict_to_be_saved):
	filename = settings.vehicles_distances_to_candidates
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


def load_vehicles_travel_times_to_candidates_dict():
	filename = settings.vehicles_travel_times_to_candidates
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict