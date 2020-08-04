# LIBRARIES
import json
from random import randint, sample, randrange, random, seed
from math import floor
from tqdm import tqdm
from deap import base, creator, tools
from sys import exit
# FILES
import settings


parameters = None


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

		# for fleet_node in parameters['recharging_nodes']:
		# 	count = 0
		# 	for duplicate_fleet_node in parameters['recharging_nodes']:
		# 		if duplicate_fleet_node == fleet_node:
		# 			count += 1
		# 	for i in range(count):
		for fleet_node in parameters['vehicles_per_recharging_node_dict']:
			for i in range(parameters['vehicles_per_recharging_node_dict'][fleet_node]):
				fleet_vehicle_node_id = str(fleet_node) + '_' + str(i)
				self.fleet_node_order.append(fleet_vehicle_node_id)
				self.x_dict['fleet_nodes'][fleet_vehicle_node_id] = dict()
				self.x_dict['fleet_nodes'][fleet_vehicle_node_id]['candidates'] = dict()
				self.x_dict['fleet_nodes'][fleet_vehicle_node_id]['existing'] = dict()
				for candidate in parameters['candidates']:
					self.x_dict['fleet_nodes'][fleet_vehicle_node_id]['candidates'][candidate] = 0
				for existing in parameters['existing']:
					self.x_dict['fleet_nodes'][fleet_vehicle_node_id]['existing'][existing] = 0
		for traffic_node in parameters['traffic_nodes']:
			for i in range(parameters['traffic_intensity'][traffic_node]):
				traffic_vehicle_node_id = str(traffic_node) + '_' + str(i)
				self.traffic_node_order.append(traffic_vehicle_node_id)
				self.x_dict['traffic_nodes'][traffic_vehicle_node_id] = dict()
				self.x_dict['traffic_nodes'][traffic_vehicle_node_id]['existing'] = dict()
				for existing in parameters['existing']:
					self.x_dict['traffic_nodes'][traffic_vehicle_node_id]['existing'][existing] = 0

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
	return json_dict


def save_json(dict_to_be_saved, filename):
	json_file = json.dumps(dict_to_be_saved)
	fp = open(filename, 'w')
	fp.write(json_file)
	fp.close()


# def reduce_input_size(list_to_be_reduced, reduced_size):
# 	reduce_sizes = True
# 	original_size = len(list_to_be_reduced)
# 	size_to_iterate = min(reduced_size, original_size)
#
# 	if reduce_sizes:
# 		reduced_list = list()
# 		for i in range(size_to_iterate):
# 			reduced_list.append(list_to_be_reduced[i])
# 		return reduced_list
# 	else:
# 		return list_to_be_reduced


def load_parameters():
	global parameters
	parameters = dict()
	candidates_dict = load_json(settings.candidates)
	candidates = [int(i) for i in candidates_dict.keys()]
	# reduced_candidates = reduce_input_size(candidates, reduced_size)
	existing_stations_dict = load_json(settings.existing_stations)
	existing = [existing_stations_dict[i]['closest_node_id'] for i in existing_stations_dict.keys()]
	# reduced_existing = reduce_input_size(existing, reduced_size)
	# existing_capacities = [existing_stations_dict[i]['chargers'] for i in existing_stations_dict.keys()]
	existing_capacities = {existing_node: existing_stations_dict[existing_node]['chargers'] for existing_node in existing_stations_dict.keys()}
	recharging_nodes = load_json(settings.recharging_nodes_list)
	vehicles_per_recharging_node_dict = load_json(settings.vehicles_per_recharging_node_dict)
	# reduced_recharging_nodes = reduce_input_size(recharging_nodes, reduced_size)
	fleet_travel_times = load_json(settings.fleet_travel_times)
	traffic_travel_times = load_json(settings.traffic_travel_times)
	traffic = load_json(settings.traffic_demand)
	traffic_nodes = list(traffic.keys())
	# reduced_traffic_nodes = reduce_input_size(traffic_nodes, reduced_size)
	# traffic_intensity = [floor(int(i) * percentage_of_evs * percentage_of_vehicles_needing_recharge) for i in list(traffic.values())]
	traffic_intensity = {i: floor(int(traffic[i]) * settings.percentage_of_evs * settings.percentage_of_vehicles_needing_recharge) for i in list(traffic.keys()) }
	rho_list = load_json(settings.rhos)
	zones = load_json(settings.zones)
	candidates_zoning = load_json(settings.candidates_zoning)
	existing_zoning = load_json(settings.existing_zoning)
	candidates_permits_dict = load_json(settings.candidate_permits_dict)

	service_rate = {'candidates': dict(), 'existing': dict()}
	for candidate_node in candidates:
		service_rate['candidates'][candidate_node] = settings.candidate_service_rate
	for existing_node in existing:
		service_rate['existing'][existing_node] = settings.existing_service_rate

	zone_bounds = load_json(settings.zone_bounds)

	land_cost = dict()
	for candidate_node in candidates:
		if candidate_node not in land_cost:
			land_cost[candidate_node] = float(candidates_permits_dict[str(candidate_node)])


	parameters['high_value'] = float('inf')
	parameters['max_chargers'] = settings.max_chargers
	parameters['candidates_zoning'] = candidates_zoning
	parameters['existing_zoning'] = existing_zoning
	parameters['candidates'] = [i for i in candidates if str(i) in list(candidates_zoning.keys())]
	parameters['existing'] = [i for i in existing if str(i) in list(existing_zoning.keys())]
	parameters['existing_capacities'] = existing_capacities
	parameters['existing_dict'] = existing_stations_dict
	parameters['recharging_nodes'] = recharging_nodes
	parameters['vehicles_per_recharging_node_dict'] = vehicles_per_recharging_node_dict
	parameters['fleet_travel_times'] = fleet_travel_times
	parameters['traffic_travel_times'] = traffic_travel_times
	parameters['traffic_nodes'] = traffic_nodes
	parameters['traffic_intensity'] = traffic_intensity
	parameters['traffic_dict'] = traffic
	parameters['service_rate'] = service_rate
	parameters['fleet_intensity'] = [1 for _ in range(len(recharging_nodes))]
	parameters['land_cost'] = land_cost
	parameters['building_cost'] = settings.charger_building_cost
	parameters['park_and_charge_cost'] = settings.annual_park_and_charge_cost
	parameters['zone_bound'] = zone_bounds
	parameters['rho'] = [float(i) for i in rho_list]
	parameters['zones'] = zones
	return parameters


def compute_equivalent_number_of_vehicles():
	n_vehicles = 0
	for recharging_node in parameters['recharging_nodes']:
		n_vehicles += parameters['vehicles_per_recharging_node_dict'][str(recharging_node)]
	return n_vehicles


def feasible_solution_exists():
	total_traffic = sum(parameters['traffic_intensity'].values())
	existing_capacities = sum(parameters['existing_capacities'].values())
	if total_traffic > existing_capacities:
		print(f'No feasible solution exists.\nTraffic: {total_traffic}, existing capacities: {existing_capacities}')
		exit()

	total_vehicles_in_nodes = sum(parameters['vehicles_per_recharging_node_dict'].values())
	total_capacities = sum(parameters['existing_capacities'].values()) + parameters['max_chargers'] * len(parameters['candidates'])
	if total_vehicles_in_nodes > total_capacities:
		print(f'No feasible solution exists.\nTotal vehicles in recharging nodes {total_vehicles_in_nodes}, total capacities: {total_capacities}')
		exit()

	total_traffic_and_vehicles_in_nodes = sum(parameters['vehicles_per_recharging_node_dict'].values()) + sum(parameters['traffic_intensity'].values())
	total_candidates_capacities = sum(parameters['existing_capacities'].values()) + parameters['max_chargers'] * len(parameters['candidates'])
	if total_traffic_and_vehicles_in_nodes  > total_candidates_capacities:
		print(f'No feasible solution exists.\nTotal traffic and vehicles in recharging nodes: {total_traffic_and_vehicles_in_nodes}, total candidate capacities: {total_candidates_capacities}')
		exit()
	return True


def get_chromosome_list(variables):
	chromosome_list = list()

	# ################## x ########################
	for fleet_node in variables.fleet_node_order:
		for candidate_node in variables.candidate_node_order:
			chromosome_list.append(variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node])
		for existing_node in variables.existing_node_order:
			chromosome_list.append(variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node])
	for traffic_node in variables.traffic_node_order:
		# for candidate_node in variables.candidate_node_order:
		# 	chromosome_list.append(variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node])
		for existing_node in variables.existing_node_order:
			chromosome_list.append(variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node])

	# ################## y ########################
	for candidate_node in variables.candidate_node_order:
		chromosome_list.append(variables.y_dict['candidates'][candidate_node])
	for existing_node in variables.existing_node_order:
		chromosome_list.append(variables.y_dict['existing'][existing_node])

	# ################## omega ########################
	for candidate_node in variables.candidate_node_order:
		chromosome_list.append(variables.omega_dict['candidates'][candidate_node])
	for existing_node in variables.existing_node_order:
		chromosome_list.append(variables.omega_dict['existing'][existing_node])

	# ################## z ########################
	for candidate_node in variables.candidate_node_order:
		for charger in range(parameters['max_chargers']):
			chromosome_list.append(variables.z_dict['candidates'][candidate_node]['chargers'][charger])
	for existing_node in variables.existing_node_order:
		for charger in range(parameters['existing_dict'][str(existing_node)]['chargers']):
			chromosome_list.append(variables.z_dict['existing'][existing_node]['chargers'][charger])
	# print(f'from dict to list: {chromosome_list}')
	return chromosome_list


def get_variable_dict(chromosome):
	global parameters
	variables = Variables(parameters)
	current_index = 0
	# ################## x ########################
	for fleet_node in variables.fleet_node_order:
		for candidate_node in variables.candidate_node_order:
			variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] = chromosome[current_index]
			current_index += 1
		for existing_node in variables.existing_node_order:
			variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node] = chromosome[current_index]
			current_index += 1
	for traffic_node in variables.traffic_node_order:
		# for candidate_node in variables.candidate_node_order:
		# 	variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node] = chromosome[current_index]
		# 	current_index += 1
		for existing_node in variables.existing_node_order:
			variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] = chromosome[current_index]
			current_index += 1

	# ################## y ########################
	for candidate_node in variables.candidate_node_order:
		variables.y_dict['candidates'][candidate_node] = chromosome[current_index]
		current_index += 1
	for existing_node in variables.existing_node_order:
		variables.y_dict['existing'][existing_node] = chromosome[current_index]
		current_index += 1

	# ################## omega ########################
	for candidate_node in variables.candidate_node_order:
		variables.omega_dict['candidates'][candidate_node] = chromosome[current_index]
		current_index += 1
	for existing_node in variables.existing_node_order:
		variables.omega_dict['existing'][existing_node] = chromosome[current_index]
		current_index += 1

	# ################## z ########################
	for candidate_node in variables.candidate_node_order:
		for charger in range(parameters['max_chargers']):
			variables.z_dict['candidates'][candidate_node]['chargers'][charger] = chromosome[current_index]
			current_index += 1
	for existing_node in variables.existing_node_order:
		for charger in range(parameters['existing_dict'][str(existing_node)]['chargers']):
			variables.z_dict['existing'][existing_node]['chargers'][charger] = chromosome[current_index]
			current_index += 1
	# print(f'from list to dict: {chromosome}')
	return variables


def queue_constraint_fulfilled(variables, candidate_node, existing_node):
	lhs, rhs = 0, 0
	if candidate_node is not None:
		for fleet_node in variables.fleet_node_order:
			lhs += variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node]
		rhs = parameters['service_rate']['candidates'][candidate_node] * (parameters['rho'][0] +
			sum((parameters['rho'][m] - parameters['rho'][m - 1]) for m in range(1, parameters['max_chargers'])))-2
		if lhs > rhs:
			return False
		else:
			return True
	else:
		for fleet_node in variables.fleet_node_order:
			lhs += variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node]
		for traffic_node in	variables.traffic_node_order:
			lhs += variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node]
		rhs = parameters['service_rate']['existing'][existing_node] * (parameters['rho'][0] +
					sum((parameters['rho'][m] - parameters['rho'][m - 1]) for m in
						range(1, parameters['existing_capacities'][str(existing_node)])))-2
		if lhs > rhs:
			return False
		else:
			return True

def generate_initial_chromosome(variables, fleet_assigned, traffic_assigned):
	print('Generating initial chromosome ...')
	shuffled_existing_list = sample(variables.existing_node_order, len(variables.existing_node_order))
	shuffled_candidates_list = sample(variables.candidate_node_order, len(variables.candidate_node_order))

	existing_availability_dict = dict()
	for existing in variables.existing_node_order:
		existing_availability_dict[existing] = dict()
		existing_availability_dict[existing]['available'] = parameters['existing_dict'][str(existing)]['chargers']
		existing_availability_dict[existing]['capacity'] = parameters['existing_dict'][str(existing)]['chargers']

	candidate_availability_dict = dict()
	for candidate_id in parameters['candidates']:
		candidate_availability_dict[candidate_id] = dict()
		candidate_availability_dict[candidate_id]['available'] = parameters['max_chargers']
		candidate_availability_dict[candidate_id]['capacity'] = parameters['max_chargers']

	# ################## x ########################
	# print('Generating x traffic ...')
	for existing in shuffled_existing_list:
		for traffic_node in variables.traffic_node_order:
			if existing_availability_dict[existing]['available'] > 0:
				if traffic_node not in traffic_assigned:
					variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing] = 1
					traffic_assigned.append(traffic_node)
					existing_availability_dict[existing]['available'] -= 1
			else:
				break

	# print('\nGenerating x fleet ...')
	for fleet_node in tqdm(variables.fleet_node_order):
		if random() <= 0.8:
			for candidate in shuffled_candidates_list:
				if candidate_availability_dict[candidate]['available'] > 0 and fleet_node not in fleet_assigned:
					variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate] = 1
					fleet_assigned.append(fleet_node)
					candidate_availability_dict[candidate]['available'] -= 1
		else:
			for existing in shuffled_existing_list:
				if existing_availability_dict[existing]['available'] > 0 and fleet_node not in fleet_assigned:
					variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing] = 1
					fleet_assigned.append(fleet_node)
					existing_availability_dict[existing]['available'] -= 1
			if fleet_node not in fleet_assigned:
				for candidate in shuffled_candidates_list:
					if candidate_availability_dict[candidate]['available'] > 0 and fleet_node not in fleet_assigned:
						variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate] = 1
						fleet_assigned.append(fleet_node)
						candidate_availability_dict[candidate]['available'] -= 1

	# ################## y ########################
	# print('Generating y ...')
	for candidate in variables.candidate_node_order:
		if candidate_availability_dict[candidate]['available'] != candidate_availability_dict[candidate]['capacity']:
			variables.y_dict['candidates'][candidate] = 1
	for existing in variables.existing_node_order:
		if existing_availability_dict[existing]['available'] != existing_availability_dict[existing]['capacity']:
			variables.y_dict['existing'][existing] = 1

	# ################## omega ########################
	# print('Generating omega ...')
	omega_availability = dict(parameters['zone_bound'])

	for existing in variables.existing_node_order:
		zone_id = parameters['existing_zoning'][str(existing)]
		assigned_traffic = sum(variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing] for traffic_node in variables.traffic_node_order)
		if assigned_traffic > 0:
			variables.omega_dict['existing'][existing] = 0
			omega_availability[zone_id] -= 1
		else:
			variables.omega_dict['existing'][existing] = 1
		if omega_availability[zone_id] < 0:
			print(f'Not enough on-street CSs available in zone {zone_id}')
			exit()

	for candidate in variables.candidate_node_order:
		zone_id = parameters['candidates_zoning'][str(candidate)]
		if omega_availability[zone_id] > 0:
			variables.omega_dict['candidates'][candidate] = 0
			omega_availability[zone_id] -= 1
		else:
			variables.omega_dict['candidates'][candidate] = 1

	# ################## z ########################
	# print('Generating z ...')
	for candidate in variables.candidate_node_order:
		n_chargers = sum(variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate] for fleet_node in variables.fleet_node_order)
		if n_chargers > 0:
			for charger in range(n_chargers):
				variables.z_dict['candidates'][candidate]['chargers'][charger] = 1
	for existing in variables.existing_node_order:
		n_chargers = sum(variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing] for fleet_node in variables.fleet_node_order)
		n_chargers += sum(variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing] for traffic_node in variables.traffic_node_order)
		for charger in range(n_chargers):
			variables.z_dict['existing'][existing]['chargers'][charger] = 1
	return get_chromosome_list(variables), fleet_assigned, traffic_assigned


def generate_initial_population(variables, population_size):
	population = list()
	fleet_assigned = list()
	traffic_assigned = list()
	for i in range(population_size):
		print(f'########################### Chromosome {i} ###########################')
		chromosome, fleet_assigned, traffic_assigned = generate_initial_chromosome(variables, fleet_assigned, traffic_assigned)
		print('Evaluating initial chromosome ...')
		chromosome_value, = evaluate_chromosome(chromosome)
		if chromosome_value == parameters['high_value']:
			print('invalid initial chromosome')
			exit()
		population.append(chromosome)
	print('==========================')
	save_json(population, settings.ga_initial_population)
	return population


def debugging_print(n_constraint):
	print_flag = True
	if print_flag:
		print(f'constraint {n_constraint}')


def evaluate_chromosome(chromosome):
	global parameters
	variables = get_variable_dict(chromosome)

	T = 0
	for fleet_node in variables.fleet_node_order:
		for candidate_node in variables.candidate_node_order:
			T += parameters['fleet_travel_times'][fleet_node.split('_')[0]][str(candidate_node)] * variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node]
		for existing_node in variables.existing_node_order:
			T += parameters['fleet_travel_times'][fleet_node.split('_')[0]][str(existing_node)] * variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node]
	for traffic_node in variables.traffic_node_order:
		# for candidate_node in variables.candidate_node_order:
		# 	T += parameters['traffic_travel_times'][traffic_node.split('_')[0]][str(candidate_node)] * variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node]
		for existing_node in variables.existing_node_order:
			T += parameters['traffic_travel_times'][traffic_node.split('_')[0]][str(existing_node)] * variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node]

	total_land_cost = sum(parameters['land_cost'][candidate_node] * variables.y_dict['candidates'][candidate_node] * variables.omega_dict['candidates'][candidate_node] for candidate_node in variables.candidate_node_order)

	total_infrastructure_cost = 0
	for candidate_node in variables.candidate_node_order:
		psi = sum(variables.z_dict['candidates'][candidate_node]['chargers'][charger] for charger in range(parameters['max_chargers']))
		total_infrastructure_cost += parameters['building_cost'] * psi * variables.omega_dict['candidates'][candidate_node]

	total_park_and_charge_cost = 0
	for candidate_node in variables.candidate_node_order:
		psi = sum(variables.z_dict['candidates'][candidate_node]['chargers'][charger] for charger in range(parameters['max_chargers']))
		total_park_and_charge_cost += parameters['park_and_charge_cost'] * psi * (1 - variables.omega_dict['candidates'][candidate_node])
	for existing_node in variables.existing_node_order:
		psi = sum(variables.z_dict['existing'][existing_node]['chargers'][charger] for charger in range(parameters['existing_dict'][str(existing_node)]['chargers']))
		total_park_and_charge_cost += parameters['park_and_charge_cost'] * psi * (1 - variables.omega_dict['existing'][existing_node])

	M = total_land_cost + total_infrastructure_cost + total_park_and_charge_cost

	objective = settings.q_time_to_monetary_units * T + M

	# constraints (10)
	for traffic_node in variables.traffic_node_order:
		lhs = sum(variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] - variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] *
			variables.omega_dict['existing'][existing_node] for existing_node in variables.existing_node_order)
		if lhs != 1:
			debugging_print('10')
			return parameters['high_value'],

	# constraints (11)
	for fleet_node in variables.fleet_node_order:
		lhs = sum(variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] for candidate_node in variables.candidate_node_order) + \
			  sum(variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node] for existing_node in variables.existing_node_order)
		if lhs != 1:
			debugging_print('11')
			return parameters['high_value'],

	# constraints (12)
	for fleet_node in variables.fleet_node_order:
		for candidate_node in variables.candidate_node_order:
			if variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] > variables.y_dict['candidates'][candidate_node]:
				debugging_print('12a')
				return parameters['high_value'],
		for existing_node in variables.existing_node_order:
			if variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node] > variables.y_dict['existing'][existing_node]:
				debugging_print('12b')
				return parameters['high_value'],

	for traffic_node in variables.traffic_node_order:
		for existing_node in variables.existing_node_order:
			if variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] > variables.y_dict['existing'][existing_node]:
				debugging_print('12c')
				return parameters['high_value'],

	# constraints (13)
	for candidate_node in variables.candidate_node_order:
		lhs = sum(variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] for fleet_node in variables.fleet_node_order)
		rhs = sum(variables.z_dict['candidates'][candidate]['chargers'][charger] for candidate in variables.candidate_node_order for charger in range(parameters['max_chargers']))
		if lhs > rhs:
			debugging_print('13a')
			return parameters['high_value'],

	for existing_node in variables.existing_node_order:
		lhs = sum(variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node] for fleet_node in variables.fleet_node_order)
		lhs += sum(variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] for traffic_node in variables.traffic_node_order)
		rhs = sum(variables.z_dict['candidates'][candidate]['chargers'][charger] for candidate in variables.candidate_node_order for charger in range(parameters['max_chargers']))
		rhs += sum(variables.z_dict['existing'][existing]['chargers'][charger] for existing in variables.existing_node_order for charger in range(parameters['existing_dict'][str(existing)]['chargers']))
		if lhs > rhs:
			debugging_print('13b')
			return parameters['high_value'],

	# constraints (14)
	for candidate_node in variables.candidate_node_order:
		for charger in range(parameters['max_chargers']):
			if charger < parameters['max_chargers'] - 1:
				if variables.z_dict['candidates'][candidate_node]['chargers'][charger + 1] > variables.z_dict['candidates'][candidate_node]['chargers'][charger]:
					debugging_print('14a')
					return parameters['high_value'],
	for existing_node in variables.existing_node_order:
		for charger in range(parameters['existing_dict'][str(existing_node)]['chargers']):
			if charger < parameters['existing_dict'][str(existing_node)]['chargers'] - 1:
				if variables.z_dict['existing'][existing_node]['chargers'][charger + 1] > variables.z_dict['existing'][existing_node]['chargers'][charger]:
					debugging_print('14b')
					return parameters['high_value'],

	# constraints (15)
	lhs, rhs = 0, 0
	for candidate_node in variables.candidate_node_order:
		lhs = sum(variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] for fleet_node in variables.fleet_node_order)
		rhs = parameters['service_rate']['candidates'][candidate_node] * (variables.z_dict['candidates'][candidate_node]['chargers'][0] * parameters['rho'][0] +
		sum(variables.z_dict['candidates'][candidate_node]['chargers'][m] * (parameters['rho'][m] - parameters['rho'][m-1]) for m in range(1, parameters['max_chargers'])))
		if lhs > rhs:
			debugging_print(f'15a: lhs is {lhs} and rhs is {rhs}')
			return parameters['high_value'],
	for existing_node in variables.existing_node_order:
		lhs = sum(variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node] for fleet_node in variables.fleet_node_order) + \
			  sum(variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] for traffic_node in variables.traffic_node_order)
		rhs = parameters['service_rate']['existing'][existing_node] * (variables.z_dict['existing'][existing_node]['chargers'][0] * parameters['rho'][0] +
		sum(variables.z_dict['existing'][existing_node]['chargers'][m] * (parameters['rho'][m] - parameters['rho'][m-1]) for m in range(1, parameters['existing_capacities'][str(existing_node)])))
		if lhs > rhs:
			debugging_print('15b')
			return parameters['high_value'],


	# constraints (16)
	for zone in parameters['zones']:
		lhs_sum = 0
		for candidate_node in variables.candidate_node_order:
			if zone == parameters['candidates_zoning'][str(candidate_node)]:
				lhs_sum += (1 - variables.omega_dict['candidates'][candidate_node]) * variables.y_dict['candidates'][candidate_node]
		if lhs_sum > parameters['zone_bound'][zone]:
			debugging_print('16')
			return parameters['high_value'],

	return objective,


def init_individual(icls, content):
	return icls(content)


def init_population(pcls, ind_init, population):
	return pcls(ind_init(c) for c in population)


def crossover(parameters, chromosome1, chromosome2):
	chromo_dict1 = get_variable_dict(chromosome1)
	chromo_dict2 = get_variable_dict(chromosome2)
	temp_x_dict = dict(chromo_dict1.x_dict)
	chromo_dict1.x_dict = dict(chromo_dict2.x_dict)
	chromo_dict2.x_dict = dict(temp_x_dict)
	chromosome1[:] = get_chromosome_list(chromo_dict1)
	chromosome2[:] = get_chromosome_list(chromo_dict2)


def find_nearest_cs(parameters, chromo_dict, fleet_node, candidate, existing):
	travel_times_from_fleet_node = parameters['fleet_travel_times'][fleet_node.split('_')[0]]
	sorted_css = [(key, value) for key, value in sorted(travel_times_from_fleet_node.items(), key=lambda item: item[1])]
	if candidate is not None:
		for item in sorted_css:
			if int(item[0]) in parameters['candidates'] and chromo_dict.y_dict['candidates'][int(item[0])] == 1:
				chromo_dict.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate] = 0
				chromo_dict.x_dict['fleet_nodes'][fleet_node]['candidates'][item[0]] = 1
				return
	else:
		for item in sorted_css:
			if int(item[0]) in parameters['existing'] and chromo_dict.y_dict['existing'][int(item[0])] == 1:
				chromo_dict.x_dict['fleet_nodes'][fleet_node]['existing'][existing] = 0
				chromo_dict.x_dict['fleet_nodes'][fleet_node]['existing'][item[0]] = 1
				return


def forced_mutation(parameters, chromosome):
	chromo_dict = get_variable_dict(chromosome)
	for fleet_node in chromo_dict.x_dict['fleet_nodes']:
		for candidate in parameters['candidates']:
			if chromo_dict.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate] == 1 and chromo_dict.y_dict['candidates'][candidate] == 1:
				find_nearest_cs(parameters, chromo_dict, fleet_node, candidate, None)
		for existing_cs in parameters['existing']:
			if chromo_dict.x_dict['fleet_nodes'][fleet_node]['existing'][existing_cs] == 1 and chromo_dict.y_dict['existing'][existing_cs] == 1:
				find_nearest_cs(parameters, chromo_dict, fleet_node, None, existing_cs)


def feasibility_check(chromosome):
	global parameters
	chromo_dict = get_variable_dict(chromosome)

	# constraints (10)
	for traffic_node in chromo_dict.traffic_node_order:
		lhs = sum(chromo_dict.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] - chromo_dict.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] *
			chromo_dict.omega_dict['existing'][existing_node] for existing_node in chromo_dict.existing_node_order)
		if lhs < 1:
			return False

	# constraints (11)
	for fleet_node in chromo_dict.fleet_node_order:
		lhs = sum(chromo_dict.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] for candidate_node in chromo_dict.candidate_node_order) + \
			  sum(chromo_dict.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node] for existing_node in chromo_dict.existing_node_order)
		if lhs < 1:
			return False

	# constraints (12)
	for fleet_node in chromo_dict.fleet_node_order:
		for candidate_node in chromo_dict.candidate_node_order:
			if chromo_dict.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] > chromo_dict.y_dict['candidates'][candidate_node]:
				return False
		for existing_node in chromo_dict.existing_node_order:
			if chromo_dict.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node] > chromo_dict.y_dict['existing'][existing_node]:
				return False

	for traffic_node in chromo_dict.traffic_node_order:
		for existing_node in chromo_dict.existing_node_order:
			if chromo_dict.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] > chromo_dict.y_dict['existing'][existing_node]:
				return False

			#################################
	# constraints (13)
	for candidate_node in chromo_dict.candidate_node_order:
		lhs = sum(chromo_dict.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] for fleet_node in chromo_dict.fleet_node_order)
		rhs = sum(chromo_dict.z_dict['candidates'][candidate]['chargers'][charger] for candidate in chromo_dict.candidate_node_order for charger in range(parameters['max_chargers']))
		if lhs > rhs:
			# debugging_print('13a')
			return False

	for existing_node in chromo_dict.existing_node_order:
		lhs = sum(chromo_dict.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node] for fleet_node in chromo_dict.fleet_node_order)
		lhs += sum(chromo_dict.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] for traffic_node in chromo_dict.traffic_node_order)
		rhs = sum(chromo_dict.z_dict['candidates'][candidate]['chargers'][charger] for candidate in chromo_dict.candidate_node_order for charger in range(parameters['max_chargers']))
		rhs += sum(chromo_dict.z_dict['existing'][existing]['chargers'][charger] for existing in chromo_dict.existing_node_order for charger in range(parameters['existing_dict'][str(existing)]['chargers']))
		if lhs > rhs:
			# debugging_print('13b')
			return False

	# constraints (14)
	for candidate_node in chromo_dict.candidate_node_order:
		for charger in range(parameters['max_chargers']):
			if charger < parameters['max_chargers'] - 1:
				if chromo_dict.z_dict['candidates'][candidate_node]['chargers'][charger + 1] > chromo_dict.z_dict['candidates'][candidate_node]['chargers'][charger]:
					# debugging_print('14a')
					return False
	for existing_node in chromo_dict.existing_node_order:
		for charger in range(parameters['existing_dict'][str(existing_node)]['chargers']):
			if charger < parameters['existing_dict'][str(existing_node)]['chargers'] - 1:
				if chromo_dict.z_dict['existing'][existing_node]['chargers'][charger + 1] > chromo_dict.z_dict['existing'][existing_node]['chargers'][charger]:
					# debugging_print('14b')
					return False

	# constraints (15)
	lhs, rhs = 0, 0
	for candidate_node in chromo_dict.candidate_node_order:
		lhs = sum(chromo_dict.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] for fleet_node in chromo_dict.fleet_node_order)
		rhs = parameters['service_rate']['candidates'][candidate_node] * (chromo_dict.z_dict['candidates'][candidate_node]['chargers'][0] * parameters['rho'][0] +
		sum(chromo_dict.z_dict['candidates'][candidate_node]['chargers'][m] * (parameters['rho'][m] - parameters['rho'][m-1]) for m in range(1, parameters['max_chargers'])))
		if lhs > rhs:
			# debugging_print('15a')
			return False
	for existing_node in chromo_dict.existing_node_order:
		lhs = sum(chromo_dict.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node] for fleet_node in chromo_dict.fleet_node_order) + \
			  sum(chromo_dict.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] for traffic_node in chromo_dict.traffic_node_order)
		rhs = parameters['service_rate']['existing'][existing_node] * (chromo_dict.z_dict['existing'][existing_node]['chargers'][0] * parameters['rho'][0] +
		sum(chromo_dict.z_dict['existing'][existing_node]['chargers'][m] * (parameters['rho'][m] - parameters['rho'][m-1]) for m in range(1, parameters['existing_capacities'][str(existing_node)])))
		if lhs > rhs:
			# debugging_print('15b')
			return False


	# constraints (16)
	for zone in parameters['zones']:
		lhs_sum = 0
		for candidate_node in chromo_dict.candidate_node_order:
			if zone == parameters['candidates_zoning'][str(candidate_node)]:
				lhs_sum += (1 - chromo_dict.omega_dict['candidates'][candidate_node]) * chromo_dict.y_dict['candidates'][candidate_node]
		if lhs_sum > parameters['zone_bound'][zone]:
			# debugging_print('16')
			return False

	return True


def get_analytical_costs(chromosome):
	global parameters
	variables = get_variable_dict(chromosome)

	T = 0
	for fleet_node in variables.fleet_node_order:
		for candidate_node in variables.candidate_node_order:
			T += parameters['fleet_travel_times'][fleet_node.split('_')[0]][str(candidate_node)] * variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node]
		for existing_node in variables.existing_node_order:
			T += parameters['fleet_travel_times'][fleet_node.split('_')[0]][str(existing_node)] * variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node]
	for traffic_node in variables.traffic_node_order:
		for existing_node in variables.existing_node_order:
			T += parameters['traffic_travel_times'][traffic_node.split('_')[0]][str(existing_node)] * variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node]

	total_land_cost = sum(parameters['land_cost'][candidate_node] * variables.y_dict['candidates'][candidate_node] * variables.omega_dict['candidates'][candidate_node] for candidate_node in variables.candidate_node_order)

	total_infrastructure_cost = 0
	for candidate_node in variables.candidate_node_order:
		psi = sum(variables.z_dict['candidates'][candidate_node]['chargers'][charger] for charger in range(parameters['max_chargers']))
		total_infrastructure_cost += parameters['building_cost'] * psi * variables.omega_dict['candidates'][candidate_node]

	total_park_and_charge_cost = 0
	for candidate_node in variables.candidate_node_order:
		psi = sum(variables.z_dict['candidates'][candidate_node]['chargers'][charger] for charger in range(parameters['max_chargers']))
		total_park_and_charge_cost += parameters['park_and_charge_cost'] * psi * (1 - variables.omega_dict['candidates'][candidate_node])
	for existing_node in variables.existing_node_order:
		psi = sum(variables.z_dict['existing'][existing_node]['chargers'][charger] for charger in range(parameters['existing_dict'][str(existing_node)]['chargers']))
		total_park_and_charge_cost += parameters['park_and_charge_cost'] * psi * (1 - variables.omega_dict['existing'][existing_node])

	return T, total_land_cost, total_infrastructure_cost, total_park_and_charge_cost


def run_genetic():
	seed(1)
	parameters = load_parameters()
	# equivalent_number_of_vehicles = compute_equivalent_number_of_vehicles()
	solution_exists = feasible_solution_exists()
	print(f'feasible solution exists: {solution_exists}')
	print('Generating Variables')
	variables = Variables(parameters)
	print('Variables generated')
	population_size = 20
	initial_guess = generate_initial_population(variables, population_size)
	# initial_guess = load_json(settings.ga_initial_population)

	n_generations = 15
	prob_crossover = 0.4
	prob_mutation = 0.6
	creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
	creator.create("Individual", list, fitness=creator.FitnessMin)

	toolbox = base.Toolbox()
	toolbox.register('individual_initialisation', init_individual, creator.Individual)
	toolbox.register('population_initialisation', init_population, list, toolbox.individual_initialisation, initial_guess)
	toolbox.register('evaluate', evaluate_chromosome)
	toolbox.register('select', tools.selTournament)
	toolbox.register('mutate', tools.mutShuffleIndexes)

	population = toolbox.population_initialisation()

	fitness_set = list(toolbox.map(toolbox.evaluate, population))
	# save_json(fitness_set, settings.ga_initial_fitness_set)
	# fitness_set = load_json(settings.ga_initial_fitness_set)
	for ind, fit in zip(population, fitness_set):
		ind.fitness.values = fit

	best_fit_list = []
	best_sol_list = []
	best_sol = None

	best_fit = float('inf')

	for gen in range(0, n_generations):
		print(f'Generation: {gen:4} | Fitness: {best_fit:.2f}')
		offspring = toolbox.select(population, len(population), tournsize=2)
		offspring = list(map(toolbox.clone, offspring))
		for child1, child2 in zip(offspring[::2], offspring[1::2]):
			if random() < prob_crossover:
				crossover(parameters, child1, child2)
				is_feasible1 = feasibility_check(child1)
				is_feasible2 = feasibility_check(child2)
				if not is_feasible1:
					forced_mutation(parameters, child1)
				if not is_feasible2:
					forced_mutation(parameters, child2)
				del child1.fitness.values
				del child2.fitness.values

		for mutant in offspring:
			if random() < prob_mutation:
				toolbox.mutate(mutant, indpb=0.01)
				del mutant.fitness.values

		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		fitness_set = map(toolbox.evaluate, invalid_ind)
		for ind, fit in zip(invalid_ind, fitness_set):
			ind.fitness.values = fit

		population[:] = offspring

		curr_best_sol = tools.selBest(population, 1)[0]
		curr_best_fit = curr_best_sol.fitness.values[0]

		if curr_best_fit < best_fit:
			best_sol = curr_best_sol
			best_fit = curr_best_fit

			best_fit_list.append(best_fit)
			best_sol_list.append(best_sol)

	if best_sol is not None:
		variables = get_variable_dict(best_sol)
		best_sol_dict = dict()
		best_sol_dict['x'] = variables.x_dict
		best_sol_dict['y'] = variables.y_dict
		best_sol_dict['omega'] = variables.omega_dict
		best_sol_dict['z'] = variables.z_dict
		save_json(best_sol_dict, settings.ga_solution)
	else:
		print('No solution')
	# print(f'Number of candidates and existing locations is {len(parameters["candidates"]) + len(parameters["existing"])}')
	# print(f'cost is {best_fit:.2f}')

	prepare_output(len(parameters["candidates"]) + len(parameters["existing"]), best_sol, best_fit)


def get_solution_outcome():
	solution = load_json(settings.ga_solution)
	solution_outcome = dict()
	solution_outcome['n_vehicles_in_candidates'] = 0
	solution_outcome['n_vehicles_in_existing'] = 0
	solution_outcome['n_candidates_opened'] = 0
	solution_outcome['n_on_street_opened'] = 0
	solution_outcome['n_off_street_opened'] = 0

	for fleet_node in solution['x']['fleet_nodes']:
		for candidate_cs in solution['x']['fleet_nodes'][fleet_node]['candidates']:
			if solution['x']['fleet_nodes'][fleet_node]['candidates'][candidate_cs] == 1:
				solution_outcome['n_vehicles_in_candidates'] += 1
		for existing_cs in solution['x']['fleet_nodes'][fleet_node]['existing']:
			if solution['x']['fleet_nodes'][fleet_node]['existing'][existing_cs] == 1:
				solution_outcome['n_vehicles_in_existing'] += 1

	for candidate_cs in solution['y']['candidates']:
		if solution['y']['candidates'][candidate_cs] == 1:
			solution_outcome['n_candidates_opened'] += 1

	for candidate_cs in solution['omega']['candidates']:
		if solution['omega']['candidates'][candidate_cs] == 1:
			solution_outcome['n_on_street_opened'] += 1
		else:
			solution_outcome['n_off_street_opened'] += 1

	return solution_outcome


def prepare_output(candidates_existing_len, best_sol, best_fit):
	outputs = dict()
	travel_time, land_cost, infrastructure_cost, park_and_charge_cost = get_analytical_costs(best_sol)
	solution_outcome = get_solution_outcome()
	outputs['costs'] = dict()
	outputs['costs']['candidates_existing_length'] = candidates_existing_len
	outputs['costs']['total_travel_time'] = travel_time
	outputs['costs']['land_cost'] = land_cost
	outputs['costs']['infrastructure_cost'] = infrastructure_cost
	outputs['costs']['park_and_charge_cost'] = park_and_charge_cost
	outputs['costs']['total_cost'] = best_fit

	outputs['outcome'] = dict()
	outputs['outcome']['n_vehicles_in_candidates'] = solution_outcome['n_vehicles_in_candidates']
	outputs['outcome']['n_vehicles_in_existing'] = solution_outcome['n_vehicles_in_existing']
	outputs['outcome']['n_candidates_opened'] = solution_outcome['n_candidates_opened']
	outputs['outcome']['n_on_street_opened'] = solution_outcome['n_on_street_opened']
	outputs['outcome']['n_off_street_opened'] = solution_outcome['n_off_street_opened']
	save_json(outputs, settings.ga_outputs)


def prepare_output_temp():
	outputs = load_json(settings.ga_outputs)
	solution_outcome = get_solution_outcome()

	outputs['outcome'] = dict()
	outputs['outcome']['n_vehicles_in_candidates'] = solution_outcome['n_vehicles_in_candidates']
	outputs['outcome']['n_vehicles_in_existing'] = solution_outcome['n_vehicles_in_existing']
	outputs['outcome']['n_candidates_opened'] = solution_outcome['n_candidates_opened']
	outputs['outcome']['n_on_street_opened'] = solution_outcome['n_on_street_opened']
	outputs['outcome']['n_off_street_opened'] = solution_outcome['n_off_street_opened']
	save_json(outputs, settings.ga_outputs)


def load_saved_solution():
	solution = load_json(settings.temp)
	get_infrastructure_cost(solution)


def get_infrastructure_cost(variables):
	parameters = load_parameters()
	total_infrastructure_cost = 0
	for candidate_node in variables['z']['candidates']:
		psi = sum(variables['z']['candidates'][candidate_node]['chargers'][charger] for charger in range(parameters['max_chargers']))
		total_infrastructure_cost += parameters['building_cost'] * psi * variables['omega']['candidates'][candidate_node]
