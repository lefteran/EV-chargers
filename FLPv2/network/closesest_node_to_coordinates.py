# LIBRARIES
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


def get_closest_node_to_coordinates(graph_nodes, latitude, longitude):
	distance = float("inf")
	closest_node = None
	for node_key, node_data in graph_nodes(data=True):
		current_distance = distanceInKm(node_data['y'], node_data['x'], float(latitude), float(longitude))
		if current_distance < distance:
			distance = current_distance
			closest_node = node_key
	return closest_node
