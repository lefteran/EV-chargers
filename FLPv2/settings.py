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
centroids = 100
fleet_size = 1000
jv_epsilon = 0.1
clusters = None
vehicles_network_locations_per_hour_dict = None
vehicles_locations_over_day = None
travel_times_over_day = None
ev_percentage = 0.25
q_time_to_monetary_units = 0.737
max_chargers = 16
alpha_probability = 0.7
b_vehicles_in_queue = 2
percentage_of_evs = 0.2
candidate_service_rate = 18				# number of vehicles that can be charged per day
existing_service_rate = 14				# number of vehicles that can be charged per day
annual_park_and_charge_cost = 6570		#in dollars/year
charger_building_cost = 60000			#in dollars/charger (including maintenance)
park_and_charge_area = 14				# a typical parking space is appx. 12 m^2 and a charge needs appx. 2m^2
percentage_of_vehicles_needing_recharge = 0.01

time_to_money = 1
N_ON = 1
N_OFF = 1


# ############################# FilePaths #############################
borough = 'Chicago'
# borough = 'Kensington'
date_of_trips = '8_1_2019'

network_json = 'data/' + borough + '/' + borough + '_network.json'
chicago_graphml_network = 'Chicago/chicago.graphml'
trip_demand = 'data/demand/' + date_of_trips + '.json'
short_trips = 'data/demand/' + date_of_trips + '_' + str(centroids) + '_centroids_short.json'
large_trips = 'data/demand/' + date_of_trips + '_' + str(centroids) + '_centroids_large.json'
trip_demand_with_network_points = 'data/demand/' + date_of_trips + '_with_network_nodes.json'
recharging_coordinates_per_hour = 'data/' + borough + '/recharging_coordinates/recharging_coordinates_per_hour_' + date_of_trips + '.json'
recharging_coordinates_list = 'data/' + borough + '/recharging_coordinates/recharging_coordinates_' + date_of_trips + '_' + str(fleet_size) + '.json'
candidates = 'data/' + borough + '/candidates/' + str(centroids) + '_centroids.json'
# recharging_nodes_per_hour = 'data/recharging_nodes/recharging_nodes_per_hour_' + date_of_trips + '.json'
recharging_nodes_list = 'data/' + borough + '/recharging_nodes/recharging_nodes_' + date_of_trips + '_' + str(fleet_size) + '.json'
vehicles_per_recharging_node_dict = 'data/' + borough + '/recharging_nodes/recharging_nodes_duplicates_' + date_of_trips + '_' + str(fleet_size) + '.json'
vehicles_distances_to_candidates = 'data/distances/' + str(fleet_size) + '_vehicles_distances_to_' + str(centroids) + '_candidates_per_hour.json'
travel_times_per_hour = 'data/travel_times/fleet_travel_times_' + date_of_trips + '.json'
fleet_travel_times = 'data/' + borough + '/travel_times/fleet_travel_times_' + date_of_trips + '_' + str(fleet_size) +  '.json'
traffic_travel_times = 'data/' + borough + '/travel_times/traffic_travel_times_' + date_of_trips + '_' + str(fleet_size) +  '.json'
statistics = 'data/chicago_vehicle_locations/statistics.json'
data_for_visualisation = 'data/data_for_visualisation/' +  algorithm_dict[algorithm] + '_solution_coordinates.json'
existing_stations_coordinates_json = 'data/existing_stations/existing_stations.json'
existing_stations_csv = 'data/existing_stations/chicago-existing-stations.csv'
existing_stations_open_chargemap = 'data/' + borough + '/existing_stations/' + borough + '_openchargemap_unique_points.json'
existing_stations = 'data/' + borough + '/existing_stations/existing_stations.json'
existing_stations_closest_nodes = 'data/existing_stations/existing-stations-closest-nodes.json'
public_stations_json = 'data/existing_stations/public_stations.json'
public_stations_closest_nodes = 'data/existing_stations/public-stations-closest-nodes.json'
traffic_counts = 'data/traffic_counts/traffic_counts_avg.csv'
traffic_demand = 'data/' + borough + '/traffic_demand/traffic_demand.json'
rhos = 'data/rhos/rhos_' + str(alpha_probability) + '_' + str(b_vehicles_in_queue) + '.json'
zoning = 'data/Chicago/chicago_zoning.geojson'
candidates_zoning = 'data/' + borough + '/' + str(centroids) + '_candidate_zoning.json'
existing_zoning = 'data/' + borough + '/zones/existing_zoning.json'
zones = 'data/' + borough + '/zones/zones.json'
zone_bounds = 'data/' + borough + '/zones/zone_bounds.json'
candidates_and_existing = 'data/candidates_and_existing/candidates_and_existing.json'
raw_building_permits = 'data/' + borough + '/building_permits/Building_Permits.csv'
building_permits = 'data/' + borough + '/building_permits/building_permits.json'
candidate_permits_dict = 'data/' + borough + '/building_permits/candidates_permits_dict.json'

customer_demand = 'data/customer_demand_by_date/' + date_of_trips.replace('-', '_') + '.json'
delos_vehicle_kpis = 'data/delos_kpis/VehicleKPIs_' + str(fleet_size) + 'vehicles.json'

continuous_solution = 'data/solutions/continuous_solution.json'
integer_solution = 'data/solutions/integer_solution.json'
ga_solution = 'data/solutions/ga_solution_' + str(fleet_size) + '_fleet_' + str(centroids) + '_candidates.json'
ga_outputs = 'data/solutions/ga_outputs_' + str(fleet_size) + '_fleet_' + str(centroids) + '_candidates.json'
ga_initial_population = 'data/solutions/intial_population_' + date_of_trips + '_' + str(fleet_size) + '.json'
ga_initial_fitness_set = 'data/solutions/fitness_set_' + date_of_trips + '_' + str(fleet_size) + '.json'
temp = 'data/solutions/variable_fleet_size/ga_solution_' + str(fleet_size) + '_fleet_' + str(centroids) + '_candidates.json'

initial_solution_path = 'data/solutions/forward_greedy/' + str(k) + 'facilities_' + str(fleet_size) + 'vehicles_' + str(centroids) + 'candidates.json'
initial_fractional_solution_path = 'data/solutions/fractional_optimal/' + str(k) + 'facilities_' + str(fleet_size) + 'vehicles_' + str(centroids) + 'candidates.json'
solution_path = 'data/solutions/' + algorithm_dict[algorithm] + '/' + str(k) + 'facilities_' + str(fleet_size) + 'vehicles_' + str(centroids) + 'candidates.json'
optimal_dat_file = 'data/travel_times/optimal_data_' + str(k) + '_facilities_' + str(fleet_size) + '_vehicles_and_' + str(centroids) + '_candidates.dat'
optimal_dat_file2020 = 'data/optimal_dat/optimal_data.dat'
mapping_for_optimal = 'data/travel_times/optimal_mapping' + str(fleet_size) + '_vehicles_and_' + str(centroids) + '_candidates_mapping.json'
