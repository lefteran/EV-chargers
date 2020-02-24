# LIBRARIES
import json
# FILES
import settings


def get_dict_of_all_travel_times_over_day(travel_times_per_hour_dict):
	day_travel_times = dict()
	for _, hour_travel_time_dict in travel_times_per_hour_dict.items():
		for travel_time_key, travel_time in hour_travel_time_dict.items():
			day_travel_times[travel_time_key] = travel_time
	return day_travel_times



def create_dat_file():
	# mapping_dict = dict()
	vehicle_mapping_dict = dict()
	centroid_mapping_dict = dict()
	vehicle_count = 1
	candidate_count = 1
	with open(settings.travel_times_per_hour, 'r') as json_file, open(settings.optimal_dat_file, "w") as dat_file:
		json_dict = json.load(json_file)
		dat_file.write(f'param k := {settings.k};\n\n\nparam t :=\n')
		day_travel_times_dict = get_dict_of_all_travel_times_over_day(json_dict)
		for origin_destination_tuple, travel_time in day_travel_times_dict.items():
			origin = origin_destination_tuple.split('-')[0]
			destination = origin_destination_tuple.split('-')[1]
			if origin not in vehicle_mapping_dict:
				origin_id = vehicle_count
				vehicle_mapping_dict[origin] = origin_id
				vehicle_count += 1
			else:
				origin_id = vehicle_mapping_dict[origin]
			if destination not in centroid_mapping_dict:
				destination_id = candidate_count
				centroid_mapping_dict[destination] = destination_id
				candidate_count += 1
			else:
				destination_id = centroid_mapping_dict[destination]
			dat_file.write(f'{origin_id} {destination_id} {travel_time}\n')
		dat_file.write(';\n\n\n')

		dat_file.write('set V := ')
		for i in range(settings.fleet_size):
			dat_file.write(f'{i+1};') if i == settings.fleet_size - 1 else dat_file.write(f'{i+1} ')
		dat_file.write('\n\n')

		dat_file.write('set C := ')
		for i in range(settings.centroids):
			dat_file.write(f'{i+1};') if i == settings.centroids - 1 else dat_file.write(f'{i+1} ')

	json_mapping_file = json.dumps(centroid_mapping_dict)
	f = open(settings.mapping_for_optimal, 'w')
	f.write(json_mapping_file)
	f.close()



