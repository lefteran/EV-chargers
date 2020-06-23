# LIBRARIES
import json
from math import sin, cos, sqrt, atan2, radians
import networkx as nx
# FILES
import settings

def distanceInKm(latitude1, longitude1, latitude2, longitude2):
	# approximate radius of earth in km
	R = 6373.0

	lat1 = radians(latitude1)
	lon1 = radians(longitude1)
	lat2 = radians(latitude2)
	lon2 = radians(longitude2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	return distance


def load_json(filename):
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return json_dict


def get_centroid_key_of_closest_cluster(graph_nodes, vehicle_latitude, vehicle_longitude, cluster_centroids):
	distance = float("inf")
	centroid_key = None
	for centroid in cluster_centroids:
		current_distance = distanceInKm(graph_nodes[int(centroid)]['y'], graph_nodes[int(centroid)]['x'], vehicle_latitude, vehicle_longitude)
		if current_distance < distance:
			distance = current_distance
			centroid_key = centroid
	return centroid_key


def get_id_of_closest_existing(graph_nodes, vehicle_latitude, vehicle_longitude, existing_ids):
	distance = float("inf")
	closest_existing_id = None
	for existing_id in existing_ids:
		current_distance = distanceInKm(graph_nodes[int(existing_id)]['y'], graph_nodes[int(existing_id)]['x'], vehicle_latitude, vehicle_longitude)
		if current_distance < distance:
			distance = current_distance
			closest_existing_id = int(existing_id)
	return closest_existing_id


def find_closest_network_node_to_vehicle_within_cluster(graph_nodes, vehicle_latitude, vehicle_longitude, clusters, centroid_key):
	distance = float("inf")
	closest_node_id = None
	cluster_nodes = clusters[centroid_key]
	for network_node_key in cluster_nodes:
		current_distance = distanceInKm(graph_nodes[network_node_key]['y'], graph_nodes[network_node_key]['x'], vehicle_latitude, vehicle_longitude)
		if current_distance < distance:
			distance = current_distance
			closest_node_id = network_node_key
	return closest_node_id


def save_recharging_nodes(dict_to_be_saved):
	filename = settings.recharging_nodes_list
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


def save_recharging_nodes_duplicates(dict_to_be_saved):
	filename = settings.vehicles_per_recharging_node_dict
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


def load_recharging_nodes_per_hour_dict():
	filename = settings.recharging_nodes_per_hour
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict


def find_recharging_nodes_per_hour_dict(graph_nodes, clusters):
	# recharging_nodes_per_hour_dict = dict()
	recharging_nodes_list = list()
	with open(settings.recharging_coordinates_list) as json_file:
		# vehicles_locations_per_hour_dict = json.load(json_file)
		vehicles_locations_list = json.load(json_file)
	for vehicle in vehicles_locations_list:
	# for hour_key, hour_value in vehicles_locations_per_hour_dict.items():
	# 	recharging_nodes_per_hour_dict[hour_key] = list()
	# 	for vehicle in hour_value:
		vehicle_coordinates = vehicle[1]
		centroid_key = get_centroid_key_of_closest_cluster(graph_nodes, vehicle_coordinates[0], vehicle_coordinates[1], list(clusters.keys()))
		node_id = find_closest_network_node_to_vehicle_within_cluster(graph_nodes, vehicle_coordinates[0], vehicle_coordinates[1], clusters, centroid_key)
		recharging_nodes_list.append(node_id)
		# recharging_nodes_per_hour_dict[hour_key].append(node_id)
	# save_recharging_nodes(recharging_nodes_per_hour_dict)
	save_recharging_nodes(recharging_nodes_list)


def find_recharging_nodes_list(graph_nodes, candidate_clusters, existing_ids_list):
	recharging_nodes_list = list()
	with open(settings.recharging_coordinates_list) as json_file:
		vehicles_locations_list = json.load(json_file)
	for vehicle in vehicles_locations_list:
		vehicle_coordinates = vehicle[1]
		centroid_key = get_centroid_key_of_closest_cluster(graph_nodes, vehicle_coordinates[0], vehicle_coordinates[1], list(candidate_clusters.keys()))
		existing_id = get_id_of_closest_existing(graph_nodes, vehicle_coordinates[0], vehicle_coordinates[1], existing_ids_list)
		distance_to_candidate_centroid = distanceInKm(graph_nodes[int(centroid_key)]['y'],
													  graph_nodes[int(centroid_key)]['x'], vehicle_coordinates[0],
													  vehicle_coordinates[1])
		distance_to_closest_existing = distanceInKm(graph_nodes[int(existing_id)]['y'],
													  graph_nodes[int(centroid_key)]['x'], vehicle_coordinates[0],
													  vehicle_coordinates[1])
		if distance_to_candidate_centroid < distance_to_closest_existing:
			node_id = find_closest_network_node_to_vehicle_within_cluster(graph_nodes, vehicle_coordinates[0], vehicle_coordinates[1], candidate_clusters, centroid_key)
		else:
			node_id = existing_id
		recharging_nodes_list.append(node_id)
	save_recharging_nodes(recharging_nodes_list)



def find_recharging_nodes_duplicates():
	recharging_nodes_list = load_json(settings.recharging_nodes_list)
	recharging_node_duplicates_dict = dict()
	for recharging_node in recharging_nodes_list:
		if recharging_node not in recharging_node_duplicates_dict:
			recharging_node_duplicates_dict[recharging_node] = 1
		else:
			recharging_node_duplicates_dict[recharging_node] += 1
	save_recharging_nodes_duplicates(recharging_node_duplicates_dict)