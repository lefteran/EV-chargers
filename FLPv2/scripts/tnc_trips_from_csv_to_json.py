import csv
import json
from datetime import datetime
from tqdm import tqdm
import os


def sort_list_by_date(trip_list):
	return sorted(trip_list, key=lambda x: datetime.strptime(x['StartTime'], '%d/%m/%Y %H:%M:%S'))

def export_one_day_data_to_csv(fixed_date):
	import_file_path = 'Taxi_Trips.csv'
	# import_file_path = 'taxi_sample.csv'
	export_file_path = '../data/taxi_data_by_date/' + fixed_date + '.csv'
	with open(import_file_path, 'r') as csv_file_to_read, open(export_file_path, 'w') as csv_file_to_write:
		csv_reader = csv.reader(csv_file_to_read, delimiter=',')
		header = next(csv_reader, None)
		csv_file_to_write.write(", ".join(str(x) for x in header))
		csv_file_to_write.write('\n')
		for row in tqdm(csv_reader):
			try:
				date_pickup = datetime.strptime(row[2].strip(), '%m/%d/%Y %I:%M:%S %p')
				if date_pickup.strftime('%d-%m-%Y') == fixed_date:
					csv_file_to_write.write(", ".join(str(x) for x in row))
					csv_file_to_write.write('\n')
			except:
				pass


def csv_to_json(directory_name, csv_filename, file_id):
	trip_dict = dict()
	with open(csv_filename) as csv_file_to_read:
		csv_reader = csv.reader(csv_file_to_read, delimiter=',')
		next(csv_reader, None)  # skip the headers

		for row in csv_reader:
			try:
				date_pickup = datetime.strptime(row[1].strip(), '%m/%d/%Y %I:%M:%S %p')
				date_drop_off = datetime.strptime(row[2].strip(), '%m/%d/%Y %I:%M:%S %p')
			except:
				date_pickup = None
				date_drop_off = None
			origin_lat = row[15].strip()
			origin_lon = row[16].strip()
			destination_lat = row[18].strip()
			destination_lon = row[19].strip()
			if date_pickup is not None and origin_lat != '' and origin_lon != "" and destination_lat != "" and destination_lon != "":
				date = str(date_pickup.day) + '_' + str(date_pickup.month) + '_' + str(date_pickup.year)

				if date not in trip_dict.keys():
					trip_dict[date] = list()

				trip_dict[date].append({'StartTime': date_pickup.strftime('%d/%m/%Y %H:%M:%S'),
										'EndTime': date_drop_off.strftime('%d/%m/%Y %H:%M:%S'),
										'OriginLat': origin_lat, 'OriginLong': origin_lon,
										'DestinationLat': destination_lat,
										'DestinationLong': destination_lon})
		csv_file_to_read.close()
		for date in trip_dict.keys():
			sorted_list = sort_list_by_date(trip_dict[date])
			trip_dict[date] = sorted_list

		save_dict(directory_name, trip_dict, file_id)


def save_dict(directory_name, dict_to_be_saved, file_id):
	if not os.path.exists(directory_name + '\\' + file_id):
		os.makedirs(directory_name + '\\' + file_id)
	for key in dict_to_be_saved.keys():
		json_file = json.dumps(dict_to_be_saved[key])
		f = open(directory_name + '\\' + file_id + '\\' + key + '.json', 'w')
		f.write(json_file)
		f.close()



# fixed_date = '24-03-2014'
# export_one_day_data_to_csv(fixed_date)
directory_name = 'D:\Chicago taxi + TNC data\TNC trips - split'
directory_path = os.path.abspath(directory_name)
for filename in os.listdir(directory_path):
	file_id = filename[10:-4]
	file_path = os.path.abspath(directory_name + '\\' + filename)
	csv_to_json(directory_name, file_path, file_id)
	print(f'Directory {file_id} done')
