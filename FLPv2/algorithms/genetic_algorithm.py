# LIBRARIES
import json
from random import randint, sample, randrange
from math import floor
from deap import base, creator, tools
# FILES
import settings


class Variables:
	def __init__(self, parameters):
		self.x_dict = dict()
		self.fleet_node_order = list()
		self.traffic_node_order = list()
		self.y_dict = dict()
		self.candidate_node_order = list()
		self.existing_node_order = list()
		self.omega_dict = dict()
		self.z_dict = dict()

		self.x_dict['fleet_nodes'] = dict()
		self.x_dict['traffic_nodes'] = dict()

		for fleet_node in parameters['recharging_nodes']:
			count = 0
			for duplicate_fleet_node in parameters['recharging_nodes']:
				if duplicate_fleet_node == fleet_node:
					count += 1
			for i in range(count):
				self.fleet_node_order.append(str(fleet_node) + '_' + str(i))
				self.x_dict['fleet_nodes'][str(fleet_node) + '_' + str(i)] = dict()
				self.x_dict['fleet_nodes'][str(fleet_node) + '_' + str(i)]['candidates'] = dict()
				self.x_dict['fleet_nodes'][str(fleet_node) + '_' + str(i)]['existing'] = dict()
				for candidate in parameters['candidates']:
					self.x_dict['fleet_nodes'][str(fleet_node) + '_' + str(i)]['candidates'][candidate] = 0
				for existing in parameters['existing']:
					self.x_dict['fleet_nodes'][str(fleet_node) + '_' + str(i)]['existing'][existing] = 0
		for traffic_node in parameters['traffic_nodes']:
			for i in range(parameters['traffic_intensity'][traffic_node]):
				self.traffic_node_order.append(str(traffic_node) + '_' + str(i))
				self.x_dict['traffic_nodes'][str(traffic_node) + '_' + str(i)] = dict()
				self.x_dict['traffic_nodes'][str(traffic_node) + '_' + str(i)]['candidates'] = dict()
				self.x_dict['traffic_nodes'][str(traffic_node) + '_' + str(i)]['existing'] = dict()
				for candidate in parameters['candidates']:
					self.x_dict['traffic_nodes'][str(traffic_node) + '_' + str(i)]['candidates'][candidate] = 0
				for existing in parameters['existing']:
					self.x_dict['traffic_nodes'][str(traffic_node) + '_' + str(i)]['existing'][existing] = 0

		self.y_dict['candidates'] = dict()
		for candidate in parameters['candidates']:
			self.candidate_node_order.append(candidate)
			self.y_dict['candidates'][candidate] = 0
		self.y_dict['existing'] = dict()
		for existing in parameters['existing']:
			self.existing_node_order.append(existing)
			self.y_dict['existing'][existing] = 0

		self.omega_dict['candidates'] = dict()
		for candidate in parameters['candidates']:
			self.omega_dict['candidates'][candidate] = 0
		self.omega_dict['existing'] = dict()
		for existing in parameters['existing']:
			self.omega_dict['existing'][existing] = 0

		self.z_dict['candidates'] = dict()
		for candidate in parameters['candidates']:
			self.z_dict['candidates'][candidate] = dict()
			self.z_dict['candidates'][candidate]['chargers'] = dict()
			for charger in range(parameters['max_chargers']):
				self.z_dict['candidates'][candidate]['chargers'][charger] = 0
		self.z_dict['existing'] = dict()
		for existing in parameters['existing']:
			self.z_dict['existing'][existing] = dict()
			self.z_dict['existing'][existing]['chargers'] = dict()
			for charger in range(parameters['existing_dict'][str(existing)]['chargers']):
				self.z_dict['existing'][existing]['chargers'][charger] = 0

	def __eq__(self, other):
		return self.x_dict == other.x_dict and self.y_dict == other.y_dict and self.omega_dict == other.omega_dict and self.z_dict == other.z_dict


def load_json(filename):
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict


def save_json(dict_to_be_saved, filename):
	json_file = json.dumps(dict_to_be_saved)
	fp = open(filename, 'w')
	fp.write(json_file)
	fp.close()


def load_parameters():
	parameters = dict()
	hour = '1'
	percentage_of_evs = 0.2
	percentage_of_vehicles_needing_recharge = 0.0005
	candidates_dict = load_json(settings.candidates)
	candidates = [int(i) for i in candidates_dict.keys()]
	existing_stations_dict = load_json(settings.existing_stations)
	existing = [existing_stations_dict[i]['closest_node_id'] for i in existing_stations_dict.keys()]
	capacities = [existing_stations_dict[i]['chargers'] for i in existing_stations_dict.keys()]
	recharging_nodes_per_hour = load_json(settings.recharging_nodes_per_hour)
	recharging_nodes = recharging_nodes_per_hour[hour]
	travel_times_per_hour = load_json(settings.travel_times_per_hour)
	fleet_travel_times = travel_times_per_hour[hour]
	traffic_travel_times = load_json(settings.traffic_travel_times)
	traffic = load_json(settings.traffic_demand)
	traffic_nodes = list(traffic.keys())
	# traffic_intensity = [floor(int(i) * percentage_of_evs * percentage_of_vehicles_needing_recharge) for i in list(traffic.values())]
	traffic_intensity = {i: floor(int(traffic[i]) * percentage_of_evs * percentage_of_vehicles_needing_recharge) for i in list(traffic.keys()) }
	rho_list = load_json(settings.rhos)
	zones = load_json(settings.zones)
	contained = load_json(settings.contained_in_zone)

	service_rate = {'candidates': dict(), 'existing': dict()}
	for candidate_node in candidates:
		service_rate['candidates'][candidate_node] = randint(5, 10)
	for existing_node in existing:
		service_rate['existing'][existing_node] = randint(5, 10)

	zone_bounds = {zone: randint(5, 15) for zone in zones}


	parameters['high_value'] = 10000000
	parameters['max_chargers'] = 15
	parameters['contained'] = contained
	parameters['candidates'] = [i for i in candidates if str(i) in list(contained.keys())]
	parameters['existing'] = existing
	parameters['existing_capacities'] = capacities
	parameters['existing_dict'] = existing_stations_dict
	parameters['recharging_nodes'] = recharging_nodes
	parameters['fleet_travel_times'] = fleet_travel_times
	parameters['traffic_travel_times'] = traffic_travel_times
	parameters['traffic_nodes'] = traffic_nodes
	parameters['traffic_intensity'] = traffic_intensity
	parameters['traffic_dict'] = traffic
	parameters['service_rate'] = service_rate
	parameters['fleet_intensity'] = [1 for _ in range(len(recharging_nodes))]
	parameters['land_cost'] = [randint(100, 300) for _ in range(len(candidates) + len(existing))]
	parameters['building_cost'] = 60000						#in dollars (includes maintenance)
	parameters['park_and_charge_cost'] = 6570 * settings.fleet_size				#in dollars/year
	parameters['zone_bound'] = zone_bounds
	parameters['rho'] = [float(i) for i in rho_list]
	parameters['zones'] = zones
	return parameters


def feasible_solution_exists(parameters):
	if sum(parameters['traffic_intensity'].values()) > sum(parameters['existing_capacities']):
			# + parameters['max_chargers'] * sum(parameters['zone_upper_bound']):
		return False
	if len(parameters['recharging_nodes']) + sum(parameters['traffic_intensity'].values()) > sum(
			parameters['existing_capacities']) + parameters['max_chargers'] * len(parameters['candidates']):
		return False
	return True


def get_chromosome_list(variables):
	chromosome_list = list()

	for fleet_node in variables.fleet_node_order:
		for candidate_node in variables.candidate_node_order:
			chromosome_list.append(variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node])
		for existing_node in variables.existing_node_order:
			chromosome_list.append(variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node])
	for traffic_node in variables.traffic_node_order:
		for candidate_node in variables.candidate_node_order:
			chromosome_list.append(variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node])
		for existing_node in variables.existing_node_order:
			chromosome_list.append(variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node])

	for candidate_node in variables.candidate_node_order:
		chromosome_list.append(variables.y_dict['candidates'][candidate_node])
	for existing_node in variables.existing_node_order:
		chromosome_list.append(variables.y_dict['existing'][existing_node])

	for candidate_node in variables.candidate_node_order:
		chromosome_list.append(variables.omega_dict['candidates'][candidate_node])
	for existing_node in variables.existing_node_order:
		chromosome_list.append(variables.omega_dict['existing'][existing_node])

	for candidate_node in variables.candidate_node_order:
		for charger in variables.z_dict['candidates'][candidate_node]['chargers'].keys():
			chromosome_list.append(variables.z_dict['candidates'][candidate_node]['chargers'][charger])
	for existing_node in variables.existing_node_order:
		for charger in variables.z_dict['existing'][existing_node]['chargers'].keys():
			chromosome_list.append(variables.z_dict['existing'][existing_node]['chargers'][charger])

	return chromosome_list


def get_variable_dict(parameters, chromosome):
	variables = Variables(parameters)
	current_index = 0
	for fleet_node in variables.fleet_node_order:
		for candidate_node in variables.candidate_node_order:
			variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] = chromosome[current_index]
			current_index += 1
		for existing_node in variables.existing_node_order:
			variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node] = chromosome[current_index]
			current_index += 1
	for traffic_node in variables.traffic_node_order:
		for candidate_node in variables.candidate_node_order:
			variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node] = chromosome[current_index]
			current_index += 1
		for existing_node in variables.existing_node_order:
			variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] = chromosome[current_index]
			current_index += 1

	for candidate_node in variables.candidate_node_order:
		variables.y_dict['candidates'][candidate_node] = chromosome[current_index]
		current_index += 1
	for existing_node in variables.existing_node_order:
		variables.y_dict['existing'][existing_node] = chromosome[current_index]
		current_index += 1

	for candidate_node in variables.candidate_node_order:
		variables.omega_dict['candidates'][candidate_node] = chromosome[current_index]
		current_index += 1
	for existing_node in variables.existing_node_order:
		variables.omega_dict['existing'][existing_node] = chromosome[current_index]
		current_index += 1

	for candidate_node in variables.candidate_node_order:
		for charger in variables.z_dict['candidates'][candidate_node]['chargers'].keys():
			variables.z_dict['candidates'][candidate_node]['chargers'][charger] = chromosome[current_index]
			current_index += 1
	for existing_node in variables.existing_node_order:
		for charger in variables.z_dict['existing'][existing_node]['chargers'].keys():
			variables.z_dict['existing'][existing_node]['chargers'][charger] = chromosome[current_index]
			current_index += 1

	return variables


# def generate_chromosome(parameters, fleet_assigned_dict, traffic_assigned_dict):
# 	chromosome = list()
# 	# ### x ###
# 	for fleet_vehicle in fleet_assigned_dict.keys():
# 		for candidate in parameters['candidates']:
# 			chromosome.append(1) if fleet_assigned_dict[fleet_vehicle] == candidate else chromosome.append(0)
# 		for existing_station in parameters['existing']:
# 			chromosome.append(1) if fleet_assigned_dict[fleet_vehicle] == existing_station else chromosome.append(0)
# 	for traffic_vehicle in traffic_assigned_dict.keys():
# 		for candidate in parameters['candidates']:
# 			chromosome.append(1) if traffic_assigned_dict[traffic_vehicle] == candidate else chromosome.append(0)
# 		for existing_station in parameters['existing']:
# 			chromosome.append(1) if traffic_assigned_dict[traffic_vehicle] == existing_station else chromosome.append(0)
# 	# ### y ###
# 	for _ in parameters['candidates']:
# 		chromosome.append(1)
# 	for _ in parameters['existing']:
# 		chromosome.append(1)
# 	# ### omega ###
# 	for _ in parameters['candidates']:
# 		chromosome.append(1)
# 	for _ in parameters['existing']:
# 		chromosome.append(1)
# 	# ### z ###
# 	for _ in parameters['candidates']:
# 		for _ in range(parameters['max_chargers']):
# 			chromosome.append(1)
# 	for _ in parameters['existing']:
# 		for _ in range(parameters['max_chargers']):
# 			chromosome.append(1)
#
# 	return chromosome



def generate_initial_chromosome(parameters, variables):
	shuffled_existing_list = sample(variables.existing_node_order, len(variables.existing_node_order))
	shuffled_candidates_list = sample(variables.candidate_node_order, len(variables.candidate_node_order))

	existing_availability_dict = dict()
	for existing in variables.existing_node_order:
		existing_availability_dict[existing] = dict()
		existing_availability_dict[existing]['available'] = parameters['existing_dict'][str(existing)]['chargers']
		existing_availability_dict[existing]['capacity'] = parameters['existing_dict'][str(existing)]['chargers']
	traffic_assigned = list()
	for existing in shuffled_existing_list:
		if existing_availability_dict[existing]['available'] > 0:
			for traffic_node in variables.traffic_node_order:
				if traffic_node not in traffic_assigned and existing_availability_dict[existing]['available'] > 0:
					variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing] = 1
					traffic_assigned.append(traffic_node)
					existing_availability_dict[existing]['available'] -= 1

	candidate_availability_dict = dict()
	for candidate_id in parameters['candidates']:
		candidate_availability_dict[candidate_id] = dict()
		candidate_availability_dict[candidate_id]['available'] = parameters['max_chargers']
		candidate_availability_dict[candidate_id]['capacity'] = parameters['max_chargers']

	fleet_assigned = list()
	for candidate in shuffled_candidates_list:
		if candidate_availability_dict[candidate]['available'] > 0:
			for fleet_node in variables.fleet_node_order:
				if fleet_node not in fleet_assigned and candidate_availability_dict[candidate]['available'] > 0:
					variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate] = 1
					fleet_assigned.append(fleet_node)
					candidate_availability_dict[candidate]['available'] -= 1


	for candidate in variables.candidate_node_order:
		variables.y_dict['candidates'][candidate] = 1
	for existing in variables.existing_node_order:
		variables.y_dict['existing'][existing] = 1


	for candidate in variables.candidate_node_order:
		variables.omega_dict['candidates'][candidate] = 1
	for existing in variables.existing_node_order:
		variables.omega_dict['existing'][existing] = 1


	for candidate in variables.candidate_node_order:
		for charger in range(parameters['max_chargers']):
			variables.z_dict['candidates'][candidate]['chargers'][charger] = 1
	for existing in variables.existing_node_order:
		for charger in range(parameters['existing_dict'][str(existing)]['chargers']):
			variables.z_dict['existing'][existing]['chargers'][charger] = 1

	return get_chromosome_list(variables)

# def generate_traffic_initial_assignment(parameters):
# 	shuffled_existing_list = sample(parameters['existing_dict'].keys(), len(parameters['existing_dict'].keys()))
# 	traffic_assigned_dict = dict()
# 	for traffic_node in parameters['traffic_nodes']:
# 		for traffic_vehicle in range(parameters['traffic_intensity'][traffic_node]):
# 			traffic_assigned_dict[str(traffic_node) + '_' + str(traffic_vehicle)] = None
#
# 	existing_availability_dict = dict()
# 	for existing_cs_id in parameters['existing_dict'].keys():
# 		existing_availability_dict[existing_cs_id] = dict()
# 		existing_availability_dict[existing_cs_id]['available'] = parameters['existing_dict'][existing_cs_id]['chargers']
# 		existing_availability_dict[existing_cs_id]['capacity'] = parameters['existing_dict'][existing_cs_id]['chargers']
#
# 	for existing_cs_id in shuffled_existing_list:
# 		if existing_availability_dict[existing_cs_id]['available'] > 0:
# 			for traffic_vehicle_id in traffic_assigned_dict.keys():
# 				if traffic_assigned_dict[traffic_vehicle_id] is None and existing_availability_dict[existing_cs_id]['available'] > 0:
# 					traffic_assigned_dict[traffic_vehicle_id] = existing_cs_id
# 					existing_availability_dict[existing_cs_id]['available'] -= 1
# 	return traffic_assigned_dict
#
#
# def generate_fleet_initial_assignment(parameters):
# 	shuffled_candidates_list = sample(parameters['candidates'], len(parameters['candidates']))
# 	fleet_assigned_dict = dict()
# 	for fleet_node in parameters['recharging_nodes']:
# 		count = 0
# 		for duplicate_fleet_node in parameters['recharging_nodes']:
# 			if duplicate_fleet_node == fleet_node:
# 				count += 1
# 		for i in range(count):
# 			fleet_assigned_dict[str(fleet_node) + '_' + str(i)] = None
#
# 	candidate_availability_dict = dict()
# 	for candidate_id in parameters['candidates']:
# 		candidate_availability_dict[candidate_id] = dict()
# 		candidate_availability_dict[candidate_id]['available'] = parameters['max_chargers']
# 		candidate_availability_dict[candidate_id]['capacity'] = parameters['max_chargers']
#
# 	for candidate_id in shuffled_candidates_list:
# 		if candidate_availability_dict[candidate_id]['available'] > 0:
# 			for fleet_vehicle_id in fleet_assigned_dict.keys():
# 				if fleet_assigned_dict[fleet_vehicle_id] is None and candidate_availability_dict[candidate_id]['available'] > 0:
# 					fleet_assigned_dict[fleet_vehicle_id] = candidate_id
# 					candidate_availability_dict[candidate_id]['available'] -= 1
# 	return fleet_assigned_dict


def generate_initial_population(parameters, variables):
	population = list()
	n_chromosomes = 5
	for _ in range(n_chromosomes):
		chromosome = generate_initial_chromosome(parameters, variables)
		population.append(chromosome)
	return population


def evaluate_chromosome(parameters, chromosome):
	variables = get_variable_dict(parameters, chromosome)

	objective = 0

	# constraints (10)
	for traffic_node in variables.traffic_node_order:
		lhs = sum(variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node] *
				  variables.omega_dict['candidates'][candidate_node] for candidate_node in variables.candidate_node_order) + \
			  sum(variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] *
			variables.omega_dict['existing'][existing_node] for existing_node in variables.existing_node_order)
		if lhs < 1:
			return parameters['high_value']

	# constraints (11)
	for fleet_node in variables.fleet_node_order:
		lhs = sum(variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] for candidate_node in variables.candidate_node_order) + \
			  sum(variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node] for existing_node in variables.existing_node_order)
		if lhs < 1:
			return parameters['high_value']

	# constraints (12)
	for fleet_node in variables.fleet_node_order:
		for candidate_node in variables.candidate_node_order:
			if variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] > variables.y_dict['candidates'][candidate_node]:
				return parameters['high_value']
		for existing_node in variables.existing_node_order:
			if variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node] > variables.y_dict['existing'][existing_node]:
				return parameters['high_value']

	for traffic_node in variables.traffic_node_order:
		for candidate_node in variables.candidate_node_order:
			if variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node] > variables.y_dict['candidates'][candidate_node]:
				return parameters['high_value']
		for existing_node in variables.existing_node_order:
			if variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] > variables.y_dict['existing'][existing_node]:
				return parameters['high_value']

	# constraints (13)
	for fleet_node in variables.fleet_node_order:
		for candidate_node in variables.candidate_node_order:
			for charger in range(parameters['max_chargers']):
				if variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] > variables.z_dict['candidates'][candidate_node]['chargers'][charger]:
					return parameters['high_value']
		for existing_node in variables.existing_node_order:
			for charger in range(parameters['existing_dict'][str(existing_node)]['chargers']):
				if variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node] > variables.z_dict['existing'][existing_node]['chargers'][charger]:
					return parameters['high_value']

	for traffic_node in variables.traffic_node_order:
		for candidate_node in variables.candidate_node_order:
			for charger in range(parameters['max_chargers']):
				if variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node] > variables.z_dict['candidates'][candidate_node]['chargers'][charger]:
					return parameters['high_value']
		for existing_node in variables.existing_node_order:
			for charger in range(parameters['existing_dict'][str(existing_node)]['chargers']):
				if variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] > variables.z_dict['existing'][existing_node]['chargers'][charger]:
					return parameters['high_value']

	# constraints (14)
	for candidate_node in variables.candidate_node_order:
		for charger in range(parameters['max_chargers']):
			if charger < parameters['max_chargers'] - 1:
				if variables.z_dict['candidates'][candidate_node]['chargers'][charger] > variables.z_dict['candidates'][candidate_node]['chargers'][charger+1]:
					return parameters['high_value']
	for existing_node in variables.existing_node_order:
		for charger in range(parameters['existing_dict'][str(existing_node)]['chargers']):
			if charger < parameters['existing_dict'][str(existing_node)]['chargers'] - 1:
				if variables.z_dict['existing'][existing_node]['chargers'][charger] > variables.z_dict['existing'][existing_node]['chargers'][charger + 1]:
					return parameters['high_value']

	# constraints (15)
	for candidate_node in variables.candidate_node_order:
		lhs = sum(variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] for fleet_node in variables.fleet_node_order) + \
			  sum(variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node] for traffic_node in variables.traffic_node_order)
		rhs = parameters['service_rate']['candidates'][candidate_node] * (variables.z_dict['candidates'][candidate_node]['chargers'][0] * parameters['rho'][0] +
		sum(variables.z_dict['candidates'][candidate_node]['chargers'][m] * (parameters['rho'][m] - parameters['rho'][m-1]) for m in range(1, parameters['max_chargers'])))
		if lhs > rhs:
			return parameters['high_value']

	# constraints (16)
	for zone in parameters['zones']:
		lhs_sum = 0
		for candidate_node in variables.candidate_node_order:
			if zone == parameters['contained'][str(candidate_node)]:
				lhs_sum += (1 - variables.omega_dict['candidates'][candidate_node]) * variables.y_dict['candidates'][candidate_node]
		if lhs_sum > parameters['zone_bound'][zone]:
			return parameters['high_value']

	return objective

def run_genetic():
	# print(f'feasible solution exists: {solution_exists}')
	parameters = load_parameters()
	variables = Variables(parameters)
	population = generate_initial_population(parameters, variables)
	for chromosome in population:
		eval = evaluate_chromosome(parameters, chromosome)
		print(eval)

	# # ############## deap ###################
	# chromosome_size = 10
	# population_size = 12
	# creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
	# creator.create("Individual", list, fitness=creator.FitnessMin)
	#
	# toolbox = base.Toolbox()
	# toolbox.register("attr_binary", randrange, 2)
	# toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_binary, n=chromosome_size)
	# toolbox.register("population", tools.initRepeat, list, toolbox.individual)

	#
	# population = toolbox.population(n= population_size)
	# a=2