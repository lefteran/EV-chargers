# import os

# ############################# Parameters #############################
algorithm = 1
algorithm_dict = {0: "integer_optimal",
				  1: "forward_greedy",
				  2: "Backward Greedy",
				  3: "Random Local Search",
				  4: "local_search",
				  5: "fractional_optimal",
				  6: "young_greedy",
				  7: "jain_vazirani"}

# places = {'london': 'Greater London, England, United Kingdom',
# 		'piedmont': 'Piedmont, California',
# 		'chicago': 'Chicago, Cook County, Illinois, USA'}


start_time = None
k = 200
centroids = 1000
fleet_size = 1000
jv_epsilon = 0.1
clusters = None
vehicles_network_locations_per_hour_dict = None
vehicles_locations_over_day = None
travel_times_over_day = None
ev_percentage = 0.25
max_chargers = 15

time_to_money = 1
N_ON = 1
N_OFF = 1


# ############################# FilePaths #############################
chicago_json_network = 'data/Chicago/Chicago_network.json'
chicago_graphml_network = 'Chicago/chicago.graphml'
date_of_trips = '8-1-2019'
trip_demand = 'data/demand/' + date_of_trips + '.json'
short_trips = 'data/demand/' + date_of_trips + '_' + str(centroids) + '_centroids_short.json'
large_trips = 'data/demand/' + date_of_trips + '_' + str(centroids) + '_centroids_large.json'
trip_demand_with_network_points = 'data/demand/' + date_of_trips + '_with_network_nodes.json'
recharging_coordinates_per_hour = 'data/recharging_coordinates/recharging_coordinates_per_hour_' + date_of_trips + '.json'
candidates = 'data/candidates/' + str(centroids) + '_centroids.json'
recharging_nodes_per_hour = 'data/recharging_nodes/recharging_nodes_per_hour_' + date_of_trips + '.json'
vehicles_distances_to_candidates = 'data/distances/' + str(fleet_size) + '_vehicles_distances_to_' + str(centroids) + '_candidates_per_hour.json'
travel_times_per_hour = 'data/travel_times/vehicles_travel_times_' + date_of_trips + '.json'
statistics = 'data/chicago_vehicle_locations/statistics.json'
data_for_visualisation = 'data/data_for_visualisation/' +  algorithm_dict[algorithm] + '_solution_coordinates.json'
existing_stations_coordinates_json = 'data/existing_stations/existing_stations.json'
existing_stations_coordinates_csv = 'data/existing_stations/chicago-existing-stations.csv'
existing_stations_closest_nodes = 'data/existing_stations/existing-stations-closest-nodes.json'
public_stations_json = 'data/existing_stations/public_stations.json'
public_stations_closest_nodes = 'data/existing_stations/public-stations-closest-nodes.json'
traffic_counts = 'data/traffic_counts/traffic_counts_avg.csv'
traffic_charging_demand = 'data/traffic_charging_demand/traffic_charging_demand.json'
rhos = 'data/rhos/rhos.json'
zoning = 'data/Chicago/chicago_zoning.geojson'
contained_in_zone = 'data/Chicago/contained.json'
zones = 'data/Chicago/zones.json'
candidates_and_existing = 'data/candidates_and_existing/candidates_and_existing.json'
continuous_solution = 'data/solutions/continuous_solution.json'
integer_solution = 'data/solutions/integer_solution.json'

initial_solution_path = 'data/solutions/forward_greedy/' + str(k) + 'facilities_' + str(fleet_size) + 'vehicles_' + str(centroids) + 'candidates.json'
initial_fractional_solution_path = 'data/solutions/fractional_optimal/' + str(k) + 'facilities_' + str(fleet_size) + 'vehicles_' + str(centroids) + 'candidates.json'
solution_path = 'data/solutions/' + algorithm_dict[algorithm] + '/' + str(k) + 'facilities_' + str(fleet_size) + 'vehicles_' + str(centroids) + 'candidates.json'
optimal_dat_file = 'data/travel_times/optimal_data_' + str(k) + '_facilities_' + str(fleet_size) + '_vehicles_and_' + str(centroids) + '_candidates.dat'
optimal_dat_file2020 = 'data/optimal_dat/optimal_data.dat'
mapping_for_optimal = 'data/travel_times/optimal_mapping' + str(fleet_size) + '_vehicles_and_' + str(centroids) + '_candidates_mapping.json'
