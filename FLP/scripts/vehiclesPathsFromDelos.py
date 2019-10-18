# LIBRARIES
from math import sin, cos, sqrt, atan2, radians
from random import uniform
import json
from sys import stderr, exit
from datetime import datetime


########## ASSUMPTIONS ##########
# 1. Vehicle range is 300 km
# 2. The battery discharges uniformly
# 3. Battery SOC after charge and arrival to customer's pick-up location is at 90% level
# 4. The threshold of the battery below which the vehicle needs recharging is 20%


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


def save_dict(dict_to_be_saved, file_location):
	json_file = json.dumps(dict_to_be_saved)
	fp = open(file_location, 'w')
	fp.write(json_file)
	fp.close()



def lists_lengths_are_equal(vehicle):
	return len(vehicle.locationList) == len(vehicle.timeStampList)


def find_charging_spots(vehicles):
	charging_spots_per_hour_dict = {key:list() for key in range(24)}
	battery_soc = uniform(0, 1)
	vehicle_range = 300
	threshold_to_charge = 0.2

	for vehicle in vehicles:
		distance_travelled = 0
		for i in range(len(vehicle.timeStampList) - 1):
			current_range = (battery_soc - threshold_to_charge) * vehicle_range
			trip_distance = distance_in_km(vehicle.locationList[i][0], vehicle.locationList[i][1],
										   vehicle.locationList[i + 1][0], vehicle.locationList[i + 1][1])

			if distance_travelled + trip_distance > current_range:
				charging_spots_per_hour_dict[vehicle.timeStampList[i].hour].append(
					(vehicle.vehicleKey, vehicle.locationList[i]))
				distance_travelled = 0
				battery_soc = 0.9
			else:
				distance_travelled += trip_distance
				current_range -= trip_distance
				battery_soc -= trip_distance / vehicle_range
	return charging_spots_per_hour_dict




filename = 'data/vehiclePaths.json'
vehPathsDict = read_json_file(filename)
vehicles = list()
for vehicleKey, vehicleValue in vehPathsDict.items():
	vehicle = Vehicle(vehicleValue['timeStampList'], vehicleValue['locationList'], vehicleKey.split(' ')[1])
	if not lists_lengths_are_equal(vehicle):
		stderr.write("Lists' lengths are not equal")
		exit()
	vehicles.append(vehicle)
charging_spots_per_hour_dict = find_charging_spots(vehicles)
save_dict(charging_spots_per_hour_dict, 'data/candidate_locations_100_vehicles.json')





