# LIBRARIES
import json
from math import sin, cos, sqrt, atan2, radians
# import graph_tool.all as gt
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


def get_centroid_key_of_closest_cluster(graph_nodes, point_latitude, point_longitude, cluster_centroids):
	distance = float("inf")
	centroid_key = None
	for centroid in cluster_centroids:
		current_distance = distanceInKm(graph_nodes[int(centroid)]['y'], graph_nodes[int(centroid)]['x'], point_latitude, point_longitude)
		if current_distance < distance:
			distance = current_distance
			centroid_key = centroid
	return centroid_key


def find_closest_network_node_to_trip_point_within_cluster(graph_nodes, point_latitude, point_longitude, clusters, centroid_key):
	distance = float("inf")
	closest_node_id = None
	cluster_nodes = clusters[centroid_key]
	for network_node_key in cluster_nodes:
		current_distance = distanceInKm(graph_nodes[network_node_key]['y'], graph_nodes[network_node_key]['x'], point_latitude, point_longitude)
		if current_distance < distance:
			distance = current_distance
			closest_node_id = network_node_key
	return closest_node_id



def filter_trips(graph, clusters):
	from tqdm import tqdm
	short_trips = list()
	large_trips = list()
	with open(settings.trip_demand, 'r') as json_file:
		trips = json.load(json_file)
	for trip in tqdm(trips):
		origin_lat = float(trip['OriginLat'])
		origin_lon = float(trip['OriginLong'])
		destination_lat = float(trip['DestinationLat'])
		destination_lon = float(trip['DestinationLong'])

		origin_centroid_key = get_centroid_key_of_closest_cluster(graph.nodes(), origin_lat, origin_lon, clusters.keys())
		origin_node_id = find_closest_network_node_to_trip_point_within_cluster(graph.nodes(), origin_lat, origin_lon, clusters, origin_centroid_key)

		destination_centroid_key = get_centroid_key_of_closest_cluster(graph.nodes(), destination_lat, destination_lon, clusters.keys())
		destination_node_id = find_closest_network_node_to_trip_point_within_cluster(graph.nodes(), destination_lat, destination_lon, clusters, destination_centroid_key)

		distance = nx.shortest_path_length(graph, source=int(origin_node_id), target=int(int(destination_node_id)), weight='length')
		if distance < 500:
			short_trips.append(trip)
		else:
			large_trips.append(trip)
	with open(settings.short_trips, 'w') as short_trip_json_file:
		short_json_file = json.dumps(short_trips)
		short_trip_json_file.write(short_json_file)
	with open(settings.large_trips, 'w') as large_trip_json_file:
		large_json_file = json.dumps(large_trips)
		large_trip_json_file.write(large_json_file)



	# for hour_key, hour_value in vehicles_locations_per_hour_dict.items():
	# 	vehicles_per_hour_dict[hour_key] = list()
	# 	for vehicle in hour_value:
	# 		vehicle_coordinates = vehicle[1]
	# 		centroid_key = get_centroid_key_of_closest_cluster(graph_nodes, vehicle_coordinates[0], vehicle_coordinates[1], clusters.keys())
	# 		node_id = find_closest_network_node_to_vehicle_within_cluster(graph_nodes, vehicle_coordinates[0], vehicle_coordinates[1], clusters, centroid_key)
	# 		vehicles_per_hour_dict[hour_key].append(node_id)
	# return vehicles_per_hour_dict


