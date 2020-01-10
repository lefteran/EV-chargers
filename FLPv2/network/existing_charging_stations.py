# LIBRARIES
import json
# FILES
import settings
import network.closesest_node_to_coordinates as closest_nodes_file


def read_json_file(filename):
	with open(filename) as json_file:
		json_dict = json.load(json_file)
	return json_dict


def import_existing_stations(graph_nodes):
	existing_stations_dict = read_json_file(settings.existing_stations_coordinates_json)
	closest_nodes_to_existing_stations_dict = dict()
	closest_nodes_to_public_stations_dict = dict()

	for existing_station_key, existing_station_info in existing_stations_dict.items():
		closest_node = closest_nodes_file.get_closest_node_to_coordinates(graph_nodes, existing_station_info['latitude'], existing_station_info['longitude'])
		closest_nodes_to_existing_stations_dict[existing_station_key] = closest_node
		if existing_station_info['type'] == 'Public':
			closest_nodes_to_public_stations_dict[existing_station_key] = closest_node
	save_closest_nodes_to_existing_stations_dict(closest_nodes_to_existing_stations_dict)
	save_closest_nodes_to_public_stations_dict(closest_nodes_to_public_stations_dict)


def find_public_stations():
	public_stations_dict = dict()
	existing_stations_dict = read_json_file(settings.existing_stations_coordinates_json)
	for existing_station_key, existing_station_info in existing_stations_dict.items():
		if existing_station_info['type'] == 'Public':
			public_stations_dict[existing_station_key] = existing_station_info
			save_public_stations_dict(public_stations_dict)


def save_public_stations_dict(dict_to_be_saved):
	filename = settings.public_stations_json
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()

def save_closest_nodes_to_public_stations_dict(dict_to_be_saved):
	filename = settings.public_stations_closest_nodes
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()

def save_closest_nodes_to_existing_stations_dict(dict_to_be_saved):
	filename = settings.existing_stations_closest_nodes
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()
