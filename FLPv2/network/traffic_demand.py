# LIBRARIES
import csv
import json
from math import ceil
# FILES
import settings
import network.closesest_node_to_coordinates as closest_node_file


def import_traffic():
	traffic_dict = dict()
	with open(settings.traffic_counts) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		next(csv_reader, None)
		for row in csv_reader:
			traffic_point_dict = dict()
			traffic_point_dict['id'] = row[0]
			traffic_point_dict['volume'] = int(ceil(float(row[4]) * settings.ev_percentage))
			traffic_point_dict['latitude'] = row[6]
			traffic_point_dict['longitude'] = row[7]
			traffic_dict[row[0]] = traffic_point_dict
	return traffic_dict


def load_json(filename):
	with open(filename) as json_file:
		json_dict = json.load(json_file)
	return json_dict


def save_traffic_demand(dict_to_be_saved):
	filename = settings.traffic_demand
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()

def compute_traffic_demand(graph):
	traffic_dict = import_traffic()
	candidates_and_existing = load_json(settings.candidates_and_existing)
	traffic_demand = dict()
	for traffic_node in traffic_dict.keys():
		nearest_station_id = None
		distance_to_nearest_station = float('inf')
		traffic_latitude = float(traffic_dict[traffic_node]['latitude'])
		traffic_longitude = float(traffic_dict[traffic_node]['longitude'])
		for candidate in candidates_and_existing:
			candidate_latitude = graph.node[int(candidate)]['y']
			candidate_longitude = graph.node[int(candidate)]['x']
			distance = closest_node_file.distanceInKm(traffic_latitude, traffic_longitude, candidate_latitude, candidate_longitude)
			if distance < distance_to_nearest_station:
				distance_to_nearest_station = distance
				nearest_station_id = candidate
		if nearest_station_id not in traffic_demand:
			traffic_demand[nearest_station_id] = traffic_dict[traffic_node]['volume']
		else:
			traffic_demand[nearest_station_id] += traffic_dict[traffic_node]['volume']
	save_traffic_demand(traffic_demand)


