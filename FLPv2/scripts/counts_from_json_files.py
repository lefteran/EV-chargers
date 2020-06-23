# LIBRARIES
import json
import os
# FILES
import settings


def load_json(filename):
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return json_dict


def count_customers():
	customers_list = load_json(settings.customer_demand)
	print(f'Number of customers: {len(customers_list)}')


def count_idle_vehicles():
	idle_vehicles = 0
	vehicle_kpis = load_json(settings.delos_vehicle_kpis)
	for vehicle in vehicle_kpis:
		if vehicle_kpis[vehicle]['VehicleTimeKpIs']['TimeTravellingToClients'] == 0.0:
			idle_vehicles += 1
	print(f'{idle_vehicles} vehicles remain idle out of {settings.fleet_size} ({float(idle_vehicles) / float(settings.fleet_size) * 100} %)')