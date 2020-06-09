# LIBRARIES
from math import sin, cos, sqrt, atan2, radians
from random import uniform
import json
from sys import stderr, exit
from datetime import datetime
import os
# FILES
import settings

########## ASSUMPTIONS ##########
# 1. Vehicle range is 180 km
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


def find_charging_points_and_total_distances_per_vehicle(vehicles):
	# charging_spots_per_hour_dict = {key:list() for key in range(24)}
	charging_spots_list = list()
	vehicle_range_km = 180
	threshold_to_charge = 0.2
	distance_travelled_per_vehicle_dict = dict()
	for vehicle in vehicles:
		total_distance_travelled = 0
		battery_soc = uniform(0.25, 1)
		distance_travelled = 0
		for i in range(len(vehicle.locationList) - 1):
			current_range = (battery_soc - threshold_to_charge) * vehicle_range_km
			trip_distance = distance_in_km(vehicle.locationList[i][0], vehicle.locationList[i][1],
										   vehicle.locationList[i + 1][0], vehicle.locationList[i + 1][1])
			total_distance_travelled += trip_distance
			if distance_travelled + trip_distance > current_range:
				charging_spots_list.append((vehicle.vehicleKey, vehicle.locationList[i]))
				# charging_spots_per_hour_dict[vehicle.timeStampList[i].hour].append((vehicle.vehicleKey, vehicle.locationList[i]))
				distance_travelled = 0
				battery_soc = 0.9
			else:
				distance_travelled += trip_distance
				current_range -= trip_distance
				battery_soc -= trip_distance / vehicle_range_km
		distance_travelled_per_vehicle_dict[vehicle.vehicleKey] = total_distance_travelled
	# return charging_spots_per_hour_dict, distance_travelled_per_vehicle_dict
	return charging_spots_list, distance_travelled_per_vehicle_dict

def get_average_distance_travelled_per_vehicle(distance_travelled_per_vehicle_dict):
	total_distances = 0
	fleet_size = 0
	for _, distance_travelled in distance_travelled_per_vehicle_dict.items():
		total_distances += distance_travelled
		fleet_size += 1
	return total_distances / float(fleet_size)


def get_number_of_vehicles_to_charge_per_day(charging_spots_per_hour_dict):
	number_of_vehicles = 0
	for _, list_of_vehicles in charging_spots_per_hour_dict.items():
		number_of_vehicles += len(list_of_vehicles)
	return number_of_vehicles


def save_statistics(dict_to_be_saved):
	filename = settings.statistics
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


def load_statistics():
	filename = settings.statistics
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict


def get_statistics(statistics_filename, n_vehicles, charging_spots_per_hour_dict, distance_travelled_per_vehicle_dict):
	fleet_statistics_dict = dict()
	average_distance_per_vehicle = get_average_distance_travelled_per_vehicle(distance_travelled_per_vehicle_dict)
	number_of_vehicles_to_charge_per_day = get_number_of_vehicles_to_charge_per_day(charging_spots_per_hour_dict)
	fleet_statistics_dict['average_distance_per_vehicle_km'] = average_distance_per_vehicle
	fleet_statistics_dict['number_of_times_vehicles_need_recharging_per_day'] = number_of_vehicles_to_charge_per_day
	if os.path.exists(statistics_filename):
		statistics_dict = load_statistics()
	else:
		statistics_dict = dict()
	statistics_dict[n_vehicles] = fleet_statistics_dict
	save_statistics(statistics_dict)


def export_charging_coordinates_per_hour_dict_and_statistics(n_vehicles, input_filename, statistics_filename, output_filename):
	allVehiclesKPIs = read_json_file(input_filename)
	vehicles = list()
	for vehicleKPIs in allVehiclesKPIs:
		vehicle = Vehicle([], allVehiclesKPIs[vehicleKPIs]['VehicleTrip'], vehicleKPIs)
		# vehicle = Vehicle(vehicleValue['timeStampList'], vehicleValue['locationList'], vehicleKey.split(' ')[1])
		# if not lists_lengths_are_equal(vehicle):
		# 	stderr.write("Lists' lengths are not equal")
		# 	exit()
		vehicles.append(vehicle)
	charging_spots_per_hour_dict, distance_travelled_per_vehicle_dict = find_charging_points_and_total_distances_per_vehicle(vehicles)
	# get_statistics(statistics_filename, n_vehicles, charging_spots_per_hour_dict, distance_travelled_per_vehicle_dict)
	# print(f'Average distance per vehicle is: {average_distance_per_vehicle} km')
	# print(f'Number of vehicles that need charging per day: {number_of_vehicles_to_charge_per_day}')
	save_dict(charging_spots_per_hour_dict, output_filename)




def slice_paths():
	input_filename = os.path.abspath('D:\Github\delos3\outputs\VehicleKPIs_' + str(settings.fleet_size) + 'vehicles.json')
	# input_filename = os.path.abspath('D:\Github\delos3\outputs\Chicago\\' + settings.date_of_trips + '\VehiclePaths.json')
	statistics_filename = 'D:\\Github\\EV-chargers\\FLPv2\\data\\chicago_vehicle_locations\\statistics.json'
	output_filename = os.path.abspath('D:\\Github\\EV-chargers\\FLPv2\\data\\recharging_coordinates\\' + 'recharging_coordinates_per_hour_' + settings.date_of_trips + '_' + str(settings.fleet_size) + '.json')
	export_charging_coordinates_per_hour_dict_and_statistics(str(settings.fleet_size), input_filename, statistics_filename, output_filename)
