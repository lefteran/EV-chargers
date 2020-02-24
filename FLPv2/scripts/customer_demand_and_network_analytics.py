import json
from datetime import datetime

def load_json(filename):
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict


def get_network_size(network):
	return len(network['nodes'])


def get_average_trip_time(demand_dict):
	format = '%d/%m/%Y %H:%M:%S'
	trips_per_hour_dict = dict()
	for hour in range(24):
		trips_per_hour_dict[hour] = 0
	n_customers = 0
	total_minutes = 0
	for customer in demand_dict:
		n_customers += 1
		start_time = customer['StartTime']
		end_time = customer['EndTime']
		tdelta = datetime.strptime(end_time, format) - datetime.strptime(start_time, format)
		minutes = (tdelta.total_seconds() % 3600) // 60
		total_minutes += minutes
		hour_of_trip = datetime.strptime(start_time, format).hour
		trips_per_hour_dict[hour_of_trip] += 1
	avg_trip_time = float(total_minutes) / float(n_customers)
	return avg_trip_time, trips_per_hour_dict


def get_analytics():
	date = '4_1_2019'
	demand_filename = 'D:\Github\EV-chargers\FLPv2\data\customer_demand_by_date\\' + date + '.json'
	demand_dict = load_json(demand_filename)
	avg_trip_time, trips_per_hour_dict = get_average_trip_time(demand_dict)
	print(f'Average trip time is {avg_trip_time} and trips per hour are')
	for hour in range(24):
		print(f'Hour {hour}: {trips_per_hour_dict[hour]}')
	network_filename = 'D:\Github\EV-chargers\FLPv2\data\Chicago\Chicago_network.json'
	network_dict = load_json(network_filename)
	network_size = get_network_size(network_dict)
	print(f'Network size is {network_size}')