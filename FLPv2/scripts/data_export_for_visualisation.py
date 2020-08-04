# LIBRARIES
import json
from datetime import datetime
from math import sin, cos, sqrt, atan2, radians
# FILES
import scripts.get_charging_points as charging_points
import settings

class Vehicle:
	def __init__(self, timeStampList, locationList, vehicleKey):
		self.vehicleKey = vehicleKey
		self.timeStampList = self.parse_timeStamp_list(timeStampList)
		self.locationList = self.parse_location_list(locationList)

	def parse_timeStamp_list(self, timeStampList):
		allTimeStamps = list()
		for time_date_stamp in timeStampList:
			time_stamp = datetime.strptime(time_date_stamp.replace('T', ' '), '%Y-%m-%d %H:%M:%S')
			allTimeStamps.append(time_stamp)
		return allTimeStamps

	def parse_location_list(self, locationList):
		visited_points = list()
		for location in locationList:
			visited_points.append((location["Latitude"], location["Longitude"]))
		return visited_points


def read_json_file(filename):
	with open(filename) as json_file:
		json_dict = json.load(json_file)
	return json_dict

def save_vehicle_route(dict_to_be_saved):
	filename = 'vehicle_route.json'
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()

def export_one_vehicle_route():
	filename = '1000vehicle-paths.json'
	vehicles_routes_dict = read_json_file(filename)
	vehicle_route = vehicles_routes_dict['Vehicle 000']['locationList']
	save_vehicle_route(vehicle_route)

def distance_in_km(latitude1, longitude1, latitude2, longitude2):
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


def save_charging_spots_coordinates(list_to_be_saved):
	filename = 'vehicle_critical_points.json'
	json_file = json.dumps(list_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()

def find_charging_spots_coordinates():
	filename = '1000vehicle-paths.json'
	vehicles_routes_dict = read_json_file(filename)
	vehicle = Vehicle(vehicles_routes_dict['Vehicle 000']['timeStampList'],
					  vehicles_routes_dict['Vehicle 000']['locationList'], '000')
	charging_spots_coordinates = list()
	vehicle_range_km = 300
	threshold_to_charge = 0.2
	total_distance_travelled = 0
	battery_soc = 0.4
	distance_travelled = 0
	for i in range(len(vehicle.timeStampList) - 1):
		current_range = (battery_soc - threshold_to_charge) * vehicle_range_km
		trip_distance = distance_in_km(vehicle.locationList[i][0], vehicle.locationList[i][1],
									   vehicle.locationList[i + 1][0], vehicle.locationList[i + 1][1])
		total_distance_travelled += trip_distance
		if distance_travelled + trip_distance > current_range:
			charging_spots_coordinates.append(vehicle.locationList[i])
			distance_travelled = 0
			battery_soc = 0.9
		else:
			distance_travelled += trip_distance
			current_range -= trip_distance
			battery_soc -= trip_distance / vehicle_range_km
	save_charging_spots_coordinates(charging_spots_coordinates)



def save_centroids_coordinates(list_to_be_saved):
	filename = 'centroids.json'
	json_file = json.dumps(list_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


def export_candidate_locations_coordinates():
	centroids_coordinates = list()
	network_filename = 'Chicago_network.json'
	clusters_filename = '1000_centroids.json'
	network = read_json_file(network_filename)
	clusters = read_json_file(clusters_filename)
	for cluster_key, _ in clusters.items():
		for node in network['nodes']:
			if cluster_key == str(node['osmid']):
				centroids_coordinates.append((node['y'], node['x']))
	save_centroids_coordinates(centroids_coordinates)


def save_solution_coordinates(list_to_be_saved):
	filename = settings.data_for_visualisation
	json_file = json.dumps(list_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


def export_solution_locations_coordinates():
	charging_points_per_station_dict = charging_points.get_number_of_charging_points_per_station()
	solution_coordinates = list()
	# algorithm = 'optimal'
	# network_filename = 'Chicago_network.json'
	# solution_filename =  algorithm + '.json'
	network = read_json_file(settings.network_json)
	# solution = read_json_file(solution_filename)
	# for node_id in solution['solution_list']:
	for node_id, number_of_charging_points in charging_points_per_station_dict.items():
		for node in network['nodes']:
			if node_id == str(node['osmid']):
				facility = {'latitude': node['y'], 'longitude': node['x'], 'charging_points': number_of_charging_points}
				solution_coordinates.append(facility)
	save_solution_coordinates(solution_coordinates)


# export_one_vehicle_route()
# find_charging_spots_coordinates()
# export_candidate_locations_coordinates()
# export_solution_locations_coordinates()