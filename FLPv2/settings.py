import os

# ############################# Parameters #############################
# facilitiesDict = {}
# zonesDict = {}
# belongingDict = {}
# adjacencyDict = {}
#
# vehiclesDict = {}
# timesDict = {}
#
# candidateLocations = []
# numberOfVehicles = 100
# radius = 0.1
# iterations = -1

# vehiclesClosestTuples = {}
# removedFacilityIds = []
# C = 1000
# r = 10000			# NUMBER OF ITERATIONS FOR THE RANDOM LOCAL SEARCH
# p = 1			# NUMBER OF FACILITIES TO SWAP (IN LS AND RANDOM LS)

algorithm = 0
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
k = 100
centroids = 1000
fleet_size = 2000
jv_epsilon = 0.1
clusters = None
vehicles_network_locations_per_hour_dict = None
travel_times = None
vehicles_locations_over_day = None
travel_times_over_day = None

# ############################# FilePaths #############################
chicago_json_network = 'data/Chicago/Chicago_network.json'
date_of_trips = '24_3_2014'
trip_demand = 'data/demand/' + date_of_trips + '.json'
short_trips = 'data/demand/' + date_of_trips + '_short.json'
large_trips = 'data/demand/' + date_of_trips + '_large.json'
trip_demand_with_network_points = 'data/demand/' + date_of_trips + '_with_network_nodes.json'
vehicles_locations_per_hour = 'data/vehicle_coordinate_locations/' + str(fleet_size) + '_vehicles_locations_per_hour.json'
cluster = 'data/clusters/' + str(centroids) + '_centroids.json'
vehicles_network_locations_per_hour = 'data/vehicles_network_locations/' + str(fleet_size) + '_vehicles_network_locations_per_hour.json'
vehicles_distances_to_candidates = 'data/distances/' + str(fleet_size) + '_vehicles_distances_to_' + str(centroids) + '_candidates_per_hour.json'
vehicles_travel_times_to_candidates = 'data/travel_times/' + str(fleet_size) + '_vehicles_travel_times_to_' + str(centroids) + '_candidates_per_hour.json'
statistics = 'data/chicago_vehicle_locations/statistics.json'

initial_solution_path = 'data/solutions/forward_greedy/' + str(k) + 'facilities_' + str(fleet_size) + 'vehicles_' + str(centroids) + 'candidates.json'
initial_fractional_solution_path = 'data/solutions/fractional_optimal/' + str(k) + 'facilities_' + str(fleet_size) + 'vehicles_' + str(centroids) + 'candidates.json'
solution_path = 'data/solutions/' + algorithm_dict[algorithm] + '/' + str(k) + 'facilities_' + str(fleet_size) + 'vehicles_' + str(centroids) + 'candidates.json'
optimal_dat_file = 'data/travel_times/optimal_data_' + str(k) + '_facilities_' + str(fleet_size) + '_vehicles_and_' + str(centroids) + '_candidates.dat'
mapping_for_optimal = 'data/travel_times/optimal_mapping' + str(fleet_size) + '_vehicles_and_' + str(centroids) + '_candidates_mapping.json'
