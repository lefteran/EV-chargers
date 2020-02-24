# LIBRARIES
import csv
import json
from math import ceil
# FILES
import settings


def load_json(filename):
	with open(filename) as json_file:
		json_dict = json.load(json_file)
	return json_dict


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



def compute_traffic_intensity():
	candidates = load_json(settings.candidates)