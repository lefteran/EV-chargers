# LIBRARIES
from math import sin, cos, sqrt, atan2, radians
import json
from sys import stderr, exit
from datetime import datetime
import os
# FILES

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



def read_json_file(filename):
	with open(filename) as json_file:
		json_dict = json.load(json_file)
	return json_dict

def find_total_distances_per_vehicle(vehicles):
	distance_travelled_per_vehicle_dict = dict()
	for vehicle in vehicles:
		total_distance_travelled = 0
		for i in range(len(vehicle.timeStampList) - 1):
			trip_distance = distance_in_km(vehicle.locationList[i][0], vehicle.locationList[i][1],
										   vehicle.locationList[i + 1][0], vehicle.locationList[i + 1][1])
			total_distance_travelled += trip_distance
		distance_travelled_per_vehicle_dict[vehicle.vehicleKey] = total_distance_travelled
	return distance_travelled_per_vehicle_dict

def get_average_distance_travelled_per_vehicle(distance_travelled_per_vehicle_dict, fleet_size):
	total_distance = 0
	if len(distance_travelled_per_vehicle_dict) != fleet_size:
		stderr.write("Fleet sizes are not equal")
		exit()
	for _, distance_travelled in distance_travelled_per_vehicle_dict.items():
		total_distance += distance_travelled
	average_distance = float(total_distance) / float(fleet_size)
	print(f'Average distance travelled is {average_distance}')


def get_average_distance_travelled(fleet_size):
	input_filename = os.path.abspath('D:\\Github\\Delos\\data\\av-chicago\\chicago_vehicle_paths\\' + str(fleet_size) + 'vehicle-paths.json')
	vehicle_paths_dict = read_json_file(input_filename)
	vehicles = list()
	for vehicleKey, vehicleValue in vehicle_paths_dict.items():
		vehicle = Vehicle(vehicleValue['timeStampList'], vehicleValue['locationList'], vehicleKey.split(' ')[1])
		vehicles.append(vehicle)
	distance_travelled_per_vehicle_dict = find_total_distances_per_vehicle(vehicles)
	get_average_distance_travelled_per_vehicle(distance_travelled_per_vehicle_dict, fleet_size)




fleet_size = 1000
get_average_distance_travelled(fleet_size)












