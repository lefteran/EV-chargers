# LIBRARIES
import json
from random import randint, sample, randrange, random, seed
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


def reduce_input_size(list_to_be_reduced):
	reduce_sizes = True
	reduced_size = 28
	original_size = len(list_to_be_reduced)
	size_to_iterate = min(reduced_size, original_size)

	if reduce_sizes:
		reduced_list = list()
		for i in range(size_to_iterate):
			reduced_list.append(list_to_be_reduced[i])
		return reduced_list
	else:
		return list_to_be_reduced


def load_parameters():
	parameters = dict()
	hour = '1'
	percentage_of_evs = 0.2
	percentage_of_vehicles_needing_recharge = 0.0005
	candidates_dict = load_json(settings.candidates)
	candidates = [int(i) for i in candidates_dict.keys()]
	reduced_candidates = reduce_input_size(candidates)
	existing_stations_dict = load_json(settings.existing_stations)
	existing = [existing_stations_dict[i]['closest_node_id'] for i in existing_stations_dict.keys()]
	reduced_existing = reduce_input_size(existing)
	capacities = [existing_stations_dict[i]['chargers'] for i in existing_stations_dict.keys()]
	recharging_nodes_per_hour = load_json(settings.recharging_nodes_per_hour)
	recharging_nodes = recharging_nodes_per_hour[hour]
	reduced_recharging_nodes = reduce_input_size(recharging_nodes)
	travel_times_per_hour = load_json(settings.travel_times_per_hour)
	fleet_travel_times = travel_times_per_hour[hour]
	traffic_travel_times = load_json(settings.traffic_travel_times)
	traffic = load_json(settings.traffic_demand)
	traffic_nodes = list(traffic.keys())
	reduced_traffic_nodes = reduce_input_size(traffic_nodes)
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

	land_cost = dict()
	for candidate_node in candidates:
		if candidate_node not in land_cost:
			land_cost[candidate_node] = randint(100, 300)
	for existing_node in existing:
		if existing_node not in land_cost:
			land_cost[existing_node] = randint(100, 300)

	parameters['high_value'] = float('inf')
	parameters['max_chargers'] = 2
	parameters['contained'] = contained
	parameters['candidates'] = [i for i in reduced_candidates if str(i) in list(contained.keys())]
	parameters['existing'] = [i for i in reduced_existing if str(i) in list(contained.keys())]
	parameters['existing_capacities'] = capacities
	parameters['existing_dict'] = existing_stations_dict
	parameters['recharging_nodes'] = reduced_recharging_nodes
	parameters['fleet_travel_times'] = fleet_travel_times
	parameters['traffic_travel_times'] = traffic_travel_times
	parameters['traffic_nodes'] = reduced_traffic_nodes
	parameters['traffic_intensity'] = traffic_intensity
	parameters['traffic_dict'] = traffic
	parameters['service_rate'] = service_rate
	parameters['fleet_intensity'] = [1 for _ in range(len(recharging_nodes))]
	parameters['land_cost'] = land_cost
	parameters['building_cost'] = 60000						#in dollars (includes maintenance)
	parameters['park_and_charge_cost'] = 6570			#in dollars/year
	parameters['zone_bound'] = zone_bounds
	parameters['rho'] = [float(i) for i in rho_list]
	parameters['zones'] = zones
	return parameters


def feasible_solution_exists(parameters):
	if sum(parameters['traffic_intensity'].values()) > sum(parameters['existing_capacities']) + parameters['max_chargers'] * sum(parameters['zone_bound']):
		return False
	if len(parameters['recharging_nodes']) + sum(parameters['traffic_intensity'].values()) > sum(
			parameters['existing_capacities']) + parameters['max_chargers'] * len(parameters['candidates']):
		return False
	return True


def get_chromosome_list(variables, parameters):
	chromosome_list = list()

	# ################## x ########################
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


def get_variable_dict(parameters, chromosome):
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
		for candidate_node in variables.candidate_node_order:
			variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node] = chromosome[current_index]
			current_index += 1
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


def generate_initial_chromosome(parameters, variables, fleet_assigned, traffic_assigned):
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
	for existing in shuffled_existing_list:
		if existing_availability_dict[existing]['available'] > 0:
			for traffic_node in variables.traffic_node_order:
				if traffic_node not in traffic_assigned:
					variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing] = 1
					traffic_assigned.append(traffic_node)
					existing_availability_dict[existing]['available'] -= 1

	for fleet_node in variables.fleet_node_order:
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
					if candidate_availability_dict[candidate]['available'] > 0:
						variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate] = 1
						fleet_assigned.append(fleet_node)
						candidate_availability_dict[candidate]['available'] -= 1

	# ################## y ########################
	for candidate in variables.candidate_node_order:
		if candidate_availability_dict[candidate]['available'] != candidate_availability_dict[candidate]['capacity']:
			variables.y_dict['candidates'][candidate] = 1
	for existing in variables.existing_node_order:
		if existing_availability_dict[existing]['available'] != existing_availability_dict[existing]['capacity']:
			variables.y_dict['existing'][existing] = 1

	# ################## omega ########################
	omega_availability = dict(parameters['zone_bound'])

	for existing in variables.existing_node_order:
		zone_id = parameters['contained'][str(existing)]
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
		zone_id = parameters['contained'][str(candidate)]
		if omega_availability[zone_id] > 0:
			variables.omega_dict['candidates'][candidate] = 0
			omega_availability[zone_id] -= 1
		else:
			variables.omega_dict['candidates'][candidate] = 1

	# ################## z ########################
	for candidate in variables.candidate_node_order:
		n_chargers = sum(variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate] for fleet_node in variables.fleet_node_order)
		if n_chargers > 0:
			for charger in range(n_chargers):
				variables.z_dict['candidates'][candidate]['chargers'][charger] = 1
	for existing in variables.existing_node_order:
		n_chargers = sum(variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing] for fleet_node in variables.fleet_node_order)
		for charger in range(n_chargers):
			variables.z_dict['existing'][existing]['chargers'][charger] = 1
	return get_chromosome_list(variables, parameters), fleet_assigned, traffic_assigned


def generate_initial_population(parameters, variables, population_size):
	population = list()
	fleet_assigned = list()
	traffic_assigned = list()
	for _ in range(population_size):
		chromosome, fleet_assigned, traffic_assigned = generate_initial_chromosome(parameters, variables, fleet_assigned, traffic_assigned)
		chromosome_value = evaluate_chromosome(parameters, chromosome)
		if chromosome_value == parameters['high_value']:
			print('invalid initial chromosome')
		population.append(chromosome)
	print('==========================')
	return population


def debugging_print(n_constraint):
	print_flag = False
	if print_flag:
		print(f'constraint {n_constraint}')


def evaluate_chromosome(parameters, chromosome):
	variables = get_variable_dict(parameters, chromosome)

	T = 0
	for fleet_node in variables.fleet_node_order:
		for candidate_node in variables.candidate_node_order:
			T += parameters['fleet_travel_times'][fleet_node.split('_')[0]][str(candidate_node)] * variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node]
		for existing_node in variables.existing_node_order:
			T += parameters['fleet_travel_times'][fleet_node.split('_')[0]][str(existing_node)] * variables.x_dict['fleet_nodes'][fleet_node]['existing'][existing_node]
	for traffic_node in variables.traffic_node_order:
		for candidate_node in variables.candidate_node_order:
			T += parameters['traffic_travel_times'][traffic_node.split('_')[0]][str(candidate_node)] * variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node]
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

	objective = T + M

	# constraints (10)
	for traffic_node in variables.traffic_node_order:
		lhs = sum(variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node] - variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node] *
				  variables.omega_dict['candidates'][candidate_node] for candidate_node in variables.candidate_node_order) + \
			  sum(variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] - variables.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] *
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
		for candidate_node in variables.candidate_node_order:
			if variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node] > variables.y_dict['candidates'][candidate_node]:
				debugging_print('12c')
				return parameters['high_value'],
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
	for candidate_node in variables.candidate_node_order:
		lhs = sum(variables.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate_node] for fleet_node in variables.fleet_node_order) + \
			  sum(variables.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node] for traffic_node in variables.traffic_node_order)
		rhs = parameters['service_rate']['candidates'][candidate_node] * (variables.z_dict['candidates'][candidate_node]['chargers'][0] * parameters['rho'][0] +
		sum(variables.z_dict['candidates'][candidate_node]['chargers'][m] * (parameters['rho'][m] - parameters['rho'][m-1]) for m in range(1, parameters['max_chargers'])))
		if lhs > rhs:
			debugging_print('15')
			return parameters['high_value'],

	# constraints (16)
	for zone in parameters['zones']:
		lhs_sum = 0
		for candidate_node in variables.candidate_node_order:
			if zone == parameters['contained'][str(candidate_node)]:
				lhs_sum += (1 - variables.omega_dict['candidates'][candidate_node]) * variables.y_dict['candidates'][candidate_node]
		if lhs_sum > parameters['zone_bound'][zone]:
			debugging_print('16')
			return parameters['high_value'],

	return objective,


def initIndividual(icls, content):
	return icls(content)


def initPopulation(pcls, ind_init, population):
	return pcls(ind_init(c) for c in population)


def crossover(parameters, chromosome1, chromosome2):
	chromo_dict1 = get_variable_dict(parameters, chromosome1)
	chromo_dict2 = get_variable_dict(parameters, chromosome2)
	temp_x_dict = dict(chromo_dict1.x_dict)
	chromo_dict1.x_dict = dict(chromo_dict2.x_dict)
	chromo_dict2.x_dict = dict(temp_x_dict)


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
	chromo_dict = get_variable_dict(parameters, chromosome)
	for fleet_node in chromo_dict.x_dict['fleet_nodes']:
		for candidate in parameters['candidates']:
			if chromo_dict.x_dict['fleet_nodes'][fleet_node]['candidates'][candidate] == 1 and chromo_dict.y_dict['candidates'][candidate] == 1:
				find_nearest_cs(parameters, chromo_dict, fleet_node, candidate, None)
		for existing_cs in parameters['existing']:
			if chromo_dict.x_dict['fleet_nodes'][fleet_node]['existing'][existing_cs] == 1 and chromo_dict.y_dict['existing'][existing_cs] == 1:
				find_nearest_cs(parameters, chromo_dict, fleet_node, None, existing_cs)


def feasibility_check(parameters, chromosome):
	chromo_dict = get_variable_dict(parameters, chromosome)

	# constraints (10)
	for traffic_node in chromo_dict.traffic_node_order:
		lhs = sum(chromo_dict.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node] - chromo_dict.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node] *
				  chromo_dict.omega_dict['candidates'][candidate_node] for candidate_node in chromo_dict.candidate_node_order) + \
			  sum(chromo_dict.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] - chromo_dict.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] *
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
		for candidate_node in chromo_dict.candidate_node_order:
			if chromo_dict.x_dict['traffic_nodes'][traffic_node]['candidates'][candidate_node] > chromo_dict.y_dict['candidates'][candidate_node]:
				return False
		for existing_node in chromo_dict.existing_node_order:
			if chromo_dict.x_dict['traffic_nodes'][traffic_node]['existing'][existing_node] > chromo_dict.y_dict['existing'][existing_node]:
				return False
	return True


def run_genetic():
	seed(1)
	parameters = load_parameters()
	solution_exists = feasible_solution_exists(parameters)
	print(f'feasible solution exists: {solution_exists}')
	variables = Variables(parameters)
	population_size = 20
	initial_guess = generate_initial_population(parameters, variables, population_size)
	n_generations = 15
	prob_crossover = 0.4
	prob_mutation = 0.6
	creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
	creator.create("Individual", list, fitness=creator.FitnessMin)

	toolbox = base.Toolbox()
	toolbox.register('individual_initialisation', initIndividual, creator.Individual)
	toolbox.register('population_initialisation', initPopulation, list, toolbox.individual_initialisation, initial_guess)
	toolbox.register('evaluate', evaluate_chromosome, parameters)
	toolbox.register('select', tools.selTournament)
	toolbox.register('mutate', tools.mutShuffleIndexes)

	population = toolbox.population_initialisation()

	fitness_set = list(toolbox.map(toolbox.evaluate, population))
	for ind, fit in zip(population, fitness_set):
		ind.fitness.values = fit

	best_fit_list = []
	best_sol_list = []
	best_sol = None

	best_fit = float('inf')

	for gen in range(0, n_generations):
		print(f'Generation: {gen:4} | Fitness: {best_fit:.2f}')
		offspring = toolbox.select(population, 2, tournsize=len(population))
		child1, child2 = list(map(toolbox.clone, offspring))
		if random() < prob_crossover:
			crossover(parameters, child1, child2)
			is_feasible1 = feasibility_check(parameters, child1)
			is_feasible2 = feasibility_check(parameters, child2)
			if not is_feasible1:
				forced_mutation(parameters, child1)
			if not is_feasible2:
				forced_mutation(parameters, child2)
			del child1.fitness.values
			del child2.fitness.values

		for chromo in offspring:
			if random() < prob_mutation:
				toolbox.mutate(chromo, indpb=0.01)
				del chromo.fitness.values

		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		fitness_set = map(toolbox.evaluate, invalid_ind)
		for ind, fit in zip(invalid_ind, fitness_set):
			ind.fitness.values = fit

		curr_best_sol = tools.selBest(population, 1)[0]
		curr_best_fit = curr_best_sol.fitness.values[0]

		if curr_best_fit < best_fit:
			best_sol = curr_best_sol
			best_fit = curr_best_fit

			best_fit_list.append(best_fit)
			best_sol_list.append(best_sol)

	if best_sol is not None:
		variables = get_variable_dict(parameters, best_sol)
		best_sol_dict = dict()
		best_sol_dict['x'] = variables.x_dict
		best_sol_dict['y'] = variables.y_dict
		best_sol_dict['omega'] = variables.omega_dict
		best_sol_dict['z'] = variables.z_dict
		save_json(best_sol_dict, settings.ga_solution)
	else:
		print('No solution')


