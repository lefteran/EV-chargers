import json
from datetime import datetime
from random import randint

def load_json(filename):
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict


def save_json(dict_to_be_saved, filename):
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


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


# Convert lats and lons from strings to floats
def edit_customer_demand_file():
	filename = 'D:\Github\delos3\data\\av-chicago\chicago_demand\\all_dates\8_1_2019.json'
	demand_file = load_json(filename)
	for trip in demand_file:
		trip['OriginLat'] = float(trip['OriginLat'])
		trip['OriginLong'] = float(trip['OriginLong'])
		trip['DestinationLat'] = float(trip['DestinationLat'])
		trip['DestinationLong'] = float(trip['DestinationLong'])
	save_json(demand_file, filename)


# Travel time and distance are added from:  D:\Github\delos3\scripts\dpy\dpy_networkdemandgen
# clear 0 distance trips
# resample minutes and seconds of the trips
# convert hours to minutes (for traveltime) and metres to km (for travel distance)
def clear_resample_and_reorder_demand():
	filename = 'D:\Github\delos3\data\\av-chicago\chicago_demand\\all_dates\8_1_2019_with_traveltime_distance.json'
	customer_demand =load_json(filename)
	cleared_and_resampled_demand = list()
	for trip in customer_demand:
		if trip['TravelTime'] != 0 and trip['TravelDistance'] != 0 and \
		   trip['TravelTime'] is not None and trip['TravelDistance'] is not None:

			trip['TravelTime'] = trip['TravelTime'] * 60
			trip['TravelDistance'] = trip['TravelDistance'] / 1000

			start_time = datetime.strptime(trip['StartTime'], '%d/%m/%Y %H:%M:%S')
			if start_time.minute == 0:
				new_start_time = start_time.replace(minute=randint(0, 14))
			elif start_time.minute == 15:
				new_start_time = start_time.replace(minute=randint(15, 29))
			elif start_time.minute == 30:
				new_start_time = start_time.replace(minute=randint(30, 44))
			elif start_time.minute == 45:
				new_start_time = start_time.replace(minute=randint(45, 59))
			start_time = new_start_time.replace(second=randint(0, 59))
			trip['StartTime'] = start_time.strftime('%d/%m/%Y %H:%M:%S')

			end_time = datetime.strptime(trip['EndTime'], '%d/%m/%Y %H:%M:%S')
			if end_time.minute == 0:
				new_end_time = end_time.replace(minute=randint(0, 14))
			elif end_time.minute == 15:
				new_end_time = end_time.replace(minute=randint(15, 29))
			elif end_time.minute == 30:
				new_end_time = end_time.replace(minute=randint(30, 44))
			elif end_time.minute == 45:
				new_end_time = end_time.replace(minute=randint(45, 59))
			end_time = new_end_time.replace(second=randint(0, 59))
			trip['EndTime'] = end_time.strftime('%d/%m/%Y %H:%M:%S')

			cleared_and_resampled_demand.append(trip)
	sorted_start_time = sorted(cleared_and_resampled_demand, key=lambda x: datetime.strptime(x['StartTime'], '%d/%m/%Y %H:%M:%S'))
	save_json(sorted_start_time, 'D:\Github\delos3\data\\av-chicago\chicago_demand\\all_dates\8_1_2019_cleared_resampled_reordered.json')


# def reorder_chronologically_start_times():
# 	import datetime
# 	customer_demand = load_json('D:\Github\delos3\data\\av-chicago\chicago_demand\\all_dates\8_1_2019_cleared_resampled.json')
# 	sorted_start_time = sorted(customer_demand, key=lambda x: datetime.datetime.strptime(x['StartTime'], '%d/%m/%Y %H:%M:%S'))
# 	save_json(sorted_start_time,
# 			  'D:\Github\delos3\data\\av-chicago\chicago_demand\\all_dates\8_1_2019_reordered_start_time.json')
