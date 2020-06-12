# LIBRARIES
import time
import json
# FILES
import settings
# import network.create_graph as create_graph
import network.recharging_nodes as vehicles_per_hour
import network.clustering as clustering
import network.shortest_paths as shortest_paths

import algorithms.fwdGreedy as fwdGreedy
# import algorithms.backGreedy as backGreedy
# import algorithms.randomLocalSearch as randomLocalSearch
# import algorithms.integer_optimal as integer_optimal
# import algorithms.fractional_optimal as fractional_optimal
import algorithms.localSearch as localSearch
import algorithms.young_greedy as young_greedy
import algorithms.jain_vazirani as jain_vazirani
# import algorithms.optimal_pulp as optimal_pulp
import algorithms.genetic_algorithm as genetic_algorithm


def run():
	genetic_algorithm.run_genetic_various_inputs()
	# optimal_pulp.solve_optimal()
	# settings.clusters = clustering.load_clusters()
	# settings.vehicles_network_locations_per_hour_dict = vehicles_per_hour.load_vehicles_network_locations_per_hour_dict()
	# settings.travel_times = shortest_paths.load_vehicles_travel_times_to_candidates_dict()
	#
	# settings.vehicles_locations_over_day = get_list_of_all_vehicles_locations_over_day()
	# settings.travel_times_over_day = get_list_of_all_travel_times_over_day()			# vehicle-candidate travel times
	#
	# solution_list = list()
	# total_driving_time = -1
	#
	# if settings.algorithm == 0:
	# 	solution_list, total_driving_time = integer_optimal.integer_optimal()
	# elif settings.algorithm == 1:
	# 	solution_list, total_driving_time = fwdGreedy.forward_greedy()
	# elif settings.algorithm == 4:
	# 	initial_solution_dict = load_solution()
	# 	solution_list, total_driving_time = localSearch.local_search(initial_solution_dict['solution_list'])
	# elif settings.algorithm == 5:
	# 	solution_list, total_driving_time = fractional_optimal.fractional_optimal()
	# elif settings.algorithm == 6:
	# 	young_greedy.young_greedy()
	# elif settings.algorithm == 7:
	# 	solution_list, total_driving_time = jain_vazirani.jv_algorithm()
	#
	# solution_dict = create_solution_dict(solution_list, settings.algorithm_dict[settings.algorithm], total_driving_time)
	# save_solution(solution_dict)


def get_list_of_all_vehicles_locations_over_day():
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



def create_solution_dict(solution_list, algorithm, total_driving_time):
	solution_dict = dict()
	solution_dict['solution_list'] = solution_list
	solution_dict['algorithm'] = algorithm
	solution_dict['total_travel_time'] = total_driving_time
	solution_dict['running_time'] = time.time() - settings.start_time
	return solution_dict


def save_solution(dict_to_be_saved):
	filename = settings.solution_path
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


def load_solution():
	filename = settings.initial_solution_path
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict