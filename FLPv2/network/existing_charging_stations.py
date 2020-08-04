# STATIONS' PARAMETERS
# https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/all/#json-output-format
# LIBRARIES
import json
import csv
from math import sin, cos, sqrt, atan2, radians
# FILES
import settings
import network.clustering as clustering


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



def load_json(filename):
	with open(filename) as json_file:
		json_dict = json.load(json_file)
	return json_dict


def save_json(dict_to_be_saved, filename):
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


def get_candidates_and_existing():
	candidates_and_existing_dict = dict()
	candidates = load_json(settings.candidates)
	existing = load_json(settings.existing_stations)
	for candidate in candidates.keys():
		candidates_and_existing_dict[candidate] = 0
	for existing_station in existing:
		candidates_and_existing_dict[existing[existing_station]['closest_node_id']] = existing[existing_station]['chargers']
	save_json(candidates_and_existing_dict, settings.candidates_and_existing)


def get_existing_stations(graph_nodes):
	existing_stations_dict = dict()
	with open(settings.existing_stations_csv) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		next(csv_reader, None)
		for row in csv_reader:
			original_station_id = row[0]
			existing_station_type = row[12]
			level_1_chargers = int(row[18]) if row[18] else 0
			level_2_chargers = int(row[19]) if row[19] else 0
			dc_chargers = int(row[20]) if row[20] else 0
			total_chargers = level_1_chargers + level_2_chargers + dc_chargers
			latitude = row[25]
			longitude = row[26]
			if 'Public' in existing_station_type and total_chargers != 0:
				existing_id = get_closest_node_to_coordinates(graph_nodes, latitude, longitude)
				if existing_id not in existing_stations_dict:
					existing_stations_dict[existing_id] = dict()
				existing_stations_dict[existing_id]['latitude'] = latitude
				existing_stations_dict[existing_id]['longitude'] = longitude
				existing_stations_dict[existing_id]['chargers'] = total_chargers
				existing_stations_dict[existing_id]['original_id'] = original_station_id
				existing_stations_dict[existing_id]['closest_node_id'] = existing_id
	save_json(existing_stations_dict, settings.existing_stations)
	get_candidates_and_existing()


def get_existing_from_open_chargemap(graph_nodes):
	existing_stations_dict = dict()
	open_chargemap_json = load_json(settings.existing_stations_open_chargemap)
	for station in open_chargemap_json:
		existing_id = get_closest_node_to_coordinates(graph_nodes, station['Coordinates']['latitude'], station['Coordinates']['longitude'])
		existing_stations_dict[existing_id] = dict()
		existing_stations_dict[existing_id]['latitude'] = station['Coordinates']['latitude']
		existing_stations_dict[existing_id]['longitude'] = station['Coordinates']['longitude']
		existing_stations_dict[existing_id]['chargers'] = 1
		existing_stations_dict[existing_id]['original_id'] = station['ID']
		existing_stations_dict[existing_id]['closest_node_id'] = int(existing_id)
	save_json(existing_stations_dict, settings.existing_stations)