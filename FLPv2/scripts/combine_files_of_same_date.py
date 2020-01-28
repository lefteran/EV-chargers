from datetime import timedelta, date, datetime
import os
import json


def load_json(filename):
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict

def sort_list_by_date(trip_list):
	return sorted(trip_list, key=lambda x: datetime.strptime(x['StartTime'], '%d/%m/%Y %H:%M:%S'))

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + timedelta(n)

def combine_files_of_same_date(the_date):
	all_trips_of_the_date_list = list()
	main_directory_name = 'D:\Chicago taxi + TNC data\TNC trips - split'
	directories_names = [d for d in os.listdir(main_directory_name) if os.path.isdir(os.path.join(main_directory_name, d))]
	for directory in directories_names:
		file_path = main_directory_name + '\\' + directory + '\\' + the_date + '.json'
		if os.path.isfile(file_path):
			few_trips_of_the_date_list = load_json(file_path)
			all_trips_of_the_date_list.extend(few_trips_of_the_date_list)
	sorted_list = sort_list_by_date(all_trips_of_the_date_list)
	save_list(sorted_list, the_date)


def save_list(list_to_be_saved, the_date):
	file_path = 'D:\Chicago taxi + TNC data\TNC trips - split\\all_dates\\' + the_date + '.json'
	json_file = json.dumps(list_to_be_saved)
	f = open(file_path, 'w')
	f.write(json_file)
	f.close()



start_date = date(2019, 1, 1)
end_date = date(2019, 3, 30)
for single_date in daterange(start_date, end_date):
	the_date = single_date.strftime("%#d_%#m_%Y")
	combine_files_of_same_date(the_date)