# LIBRARIES
import json
import csv
from math import sin, cos, sqrt, atan2, radians
from tqdm import tqdm
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


def save_json(dict_to_be_saved, filename):
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


def load_json(filename):
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict


def building_permits_to_json():
	building_permits_dict = dict()
	with open(settings.raw_building_permits) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		next(csv_reader, None)
		for row in csv_reader:
			permit_type = row[2]
			if permit_type == 'PERMIT - NEW CONSTRUCTION':
				permit_data = dict()
				permit_id = row[0]
				if row[116] and row[117]:
					permit_data['latitude'] = row[116]
					permit_data['longitude'] = row[117]
					permit_data['total_fee'] = row[24]
					building_permits_dict[permit_id] = permit_data
		save_json(building_permits_dict, settings.building_permits)



def get_candidates_land_costs_dict(graph_nodes, candidates):
	candidates_land_costs_dict = dict()
	building_permits_dict = load_json(settings.building_permits)
	for candidate in tqdm(candidates):
		candidate_lat = graph_nodes[int(candidate)]['y']
		candidate_lon = graph_nodes[int(candidate)]['x']
		closest_permit = None
		distance_to_permit = float('inf')
		for permit in building_permits_dict:
			# print(f'candidate is {candidate} and permit is {permit}')
			permit_lat = float(building_permits_dict[permit]['latitude'])
			permit_lon = float(building_permits_dict[permit]['longitude'])
			distance = distanceInKm(candidate_lat, candidate_lon, permit_lat, permit_lon)
			if distance < distance_to_permit:
				distance_to_permit = distance
				closest_permit = building_permits_dict[permit]
		candidates_land_costs_dict[candidate] = closest_permit['total_fee']
	save_json(candidates_land_costs_dict, settings.candidate_permits_dict)

