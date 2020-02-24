# LIBRARIES
import json
# FILES
import settings
import network.recharging_nodes as vehicles_per_hour
import network.shortest_paths as shortest_paths

def load_solution_dict():
	filename = settings.solution_path
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict


def get_list_of_all_vehicles_locations_over_day():
	settings.vehicles_network_locations_per_hour_dict = vehicles_per_hour.load_recharging_nodes_per_hour_dict()
	vehicles_locations = list()
	for _, vehicles_per_hour_list in settings.vehicles_network_locations_per_hour_dict.items():
		vehicles_locations.extend(vehicles_per_hour_list)
	return list(set(vehicles_locations))

def get_list_of_all_travel_times_over_day():
	day_travel_times = dict()
	for _, hour_travel_time_dict in settings.travel_times_per_hour.items():
		for travel_time_key, travel_time in hour_travel_time_dict.items():
			day_travel_times[travel_time_key] = travel_time
	return day_travel_times

def get_nearest_facility_to_vehicle(vehicle_location, locations):
	time_to_nearest_location = float("inf")
	nearest_facility = None
	for candidate_location in locations:
		travel_time = settings.travel_times_over_day[str(vehicle_location) + '-' + str(candidate_location)]
		if travel_time < time_to_nearest_location:
			time_to_nearest_location = travel_time
			nearest_facility = candidate_location
	return nearest_facility


def get_number_of_charging_points_per_station():
	settings.travel_times_per_hour = shortest_paths.load_vehicles_travel_times_to_candidates_dict()
	settings.travel_times_over_day = get_list_of_all_travel_times_over_day()		# vehicle-candidate travel times
	vehicles_locations_list = get_list_of_all_vehicles_locations_over_day()
	solution_dict = load_solution_dict()
	facility_locations = solution_dict['solution_list']

	vehicle_counter_per_facility_dict = {facility_id: 0 for facility_id in facility_locations}
	for vehicle_id in vehicles_locations_list:
		nearest_facility = get_nearest_facility_to_vehicle(vehicle_id, facility_locations)
		vehicle_counter_per_facility_dict[nearest_facility] += 1
	return vehicle_counter_per_facility_dict