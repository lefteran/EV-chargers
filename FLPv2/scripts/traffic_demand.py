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


def read_json_file(filename):
	with open(filename) as json_file:
		json_dict = json.load(json_file)
	return json_dict

def compute_traffic_demand():
	traffic_dict = import_traffic()
	public_stations_dict = read_json_file(settings.public_stations_json)
	public_stations_closest_node_mapping = read_json_file(settings.public_stations_closest_nodes)

	traffic_demand = dict()
	for traffic_key, traffic_info in traffic_dict.items():
		nearest_station_id = None
		distance_to_nearest_station = float('inf')
		traffic_latitude = float(traffic_info['latitude'])
		traffic_longitude = float(traffic_info['longitude'])
		for public_station_key, public_station_info in public_stations_dict.items():
			public_station_latitude = float(public_station_info['latitude'])
			public_station_longitude = float(public_station_info['longitude'])
			distance = closest_node_file.distanceInKm(traffic_latitude, traffic_longitude, public_station_latitude, public_station_longitude)
			if distance < distance_to_nearest_station:
				distance_to_nearest_station = distance
				nearest_station_id = public_station_key
		if nearest_station_id not in traffic_demand:
			traffic_demand[public_stations_closest_node_mapping[nearest_station_id]] = traffic_info['volume']
		else:
			traffic_demand[public_stations_closest_node_mapping[nearest_station_id]] += traffic_info['volume']
	save_traffic_demand(traffic_demand)


def save_traffic_demand(dict_to_be_saved):
	filename = settings.traffic_charging_demand
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()
