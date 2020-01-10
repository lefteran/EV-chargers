# STATIONS' PARAMETERS
# https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/all/#json-output-format
# LIBRARIES
import json
import csv
# FILES
import settings

def export_csv_to_json():
	existing_stations_dict = dict()
	with open(settings.existing_stations_coordinates_csv) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		next(csv_reader, None)
		for row in csv_reader:
			station_attributes_dict = dict()
			station_attributes_dict['id'] = row[0]
			station_attributes_dict['type'] = row[12]
			station_attributes_dict['access_time'] = row[13]
			station_attributes_dict['level_1_chargers'] = row[18]
			station_attributes_dict['level_2_chargers'] = row[19]
			station_attributes_dict['dc_chargers'] = row[20]
			station_attributes_dict['latitude'] = row[25]
			station_attributes_dict['longitude'] = row[26]
			existing_stations_dict[row[0]] = station_attributes_dict
	save_existing_stations_to_json(existing_stations_dict)


def save_existing_stations_to_json(dict_to_be_saved):
	filename = settings.existing_stations_coordinates_json
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()