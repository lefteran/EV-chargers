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



def get_centroid_key_of_closest_cluster(graph_nodes, vehicle_latitude, vehicle_longitude, cluster_centroids):
	distance = float("inf")
	centroid_key = None
	for centroid in cluster_centroids:
		current_distance = distanceInKm(graph_nodes[centroid]['y'], graph_nodes[centroid]['x'], vehicle_latitude, vehicle_longitude)
		if current_distance < distance:
			distance = current_distance
			centroid_key = centroid
	return centroid_key


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




def get_vehicles_network_locations_per_hour_dict(clusters, graph_nodes):
	vehicles_per_hour_dict = dict()
	with open(settings.vehicles_locations_per_hour) as json_file:
		vehicles_locations_per_hour_dict = json.load(json_file)
	for hour_key, hour_value in vehicles_locations_per_hour_dict.items():
		vehicles_per_hour_dict[hour_key] = list()
		for vehicle in hour_value:
			vehicle_coordinates = vehicle[1]
			centroid_key = get_centroid_key_of_closest_cluster(graph_nodes, vehicle_coordinates[0], vehicle_coordinates[1], clusters.keys())
			node_id = find_closest_network_node_to_vehicle_within_cluster(graph_nodes, vehicle_coordinates[0], vehicle_coordinates[1], clusters, centroid_key)
			vehicles_per_hour_dict[hour_key].append(node_id)
	return vehicles_per_hour_dict



