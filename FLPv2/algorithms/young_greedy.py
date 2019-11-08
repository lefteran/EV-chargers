# LIBRARIES
import json
# FILES
import settings


def get_objective_value_of_fractional_solution():
	fractional_solution_dict = load_fractional_solution()
	objective_value = fractional_solution_dict['total_travel_time']
	return objective_value


def young_greedy():
	T_f = get_objective_value_of_fractional_solution()
	ell = dict()
	phi = dict()

	for vehicle_location in settings.vehicles_locations_over_day:
		ell[vehicle_location] = None

	# for location in settings.clusters.keys():

# dict for l_i



def load_fractional_solution():
	filename = settings.initial_fractional_solution_path
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict