import json


def read_json_file(filename):
	with open(filename) as json_file:
		json_dict = json.load(json_file)
	return json_dict

def save_vehicle_routes_without_timestamps(dict_to_be_saved):
	filename = 'data/delos_paths/1000vehicle-paths-without-timestamps.json'
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


def remove_timestamps():
	filename = 'data/delos_paths/1000vehicle-paths.json'
	json_dict = read_json_file(filename)
	vehicle_spatial_data_dict = dict()
	for vehicle_key, vehicle_value in json_dict.items():
		vehicle_spatial_data_dict[vehicle_key] = vehicle_value['locationList']
	save_vehicle_routes_without_timestamps(vehicle_spatial_data_dict)

