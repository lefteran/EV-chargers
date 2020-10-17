# LIBRARIES
from pulp import *
import json
import time
from random import randint
from math import floor
# FILES
import settings

def load_json(filename):
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict


def save_formulation(prob):
	fp = open(settings.optimal_formulation, 'w')
	print(prob, file=fp)
	fp.close()


def save_solution(dict_to_be_saved, variable_space):
	if variable_space == 'Continuous':
		filename = settings.continuous_solution
	else:
		filename = settings.integer_solution
	json_file = json.dumps(dict_to_be_saved)
	fp = open(filename, 'w')
	fp.write(json_file)
	fp.close()


def load_ilp_parameters():
	parameters = dict()

	candidates_zoning = load_json(settings.candidates_zoning)
	candidates_dict = load_json(settings.candidates)
	candidates = [int(i) for i in candidates_dict.keys()]
	existing_stations_dict = load_json(settings.existing_stations)
	existing = [existing_stations_dict[i]['closest_node_id'] for i in existing_stations_dict.keys()]
	existing_zoning = load_json(settings.existing_zoning)
	existing_capacities = {existing_node: existing_stations_dict[existing_node]['chargers'] for existing_node in
						   existing_stations_dict.keys()}
	recharging_nodes = load_json(settings.recharging_nodes_list)
	vehicles_per_recharging_node_dict = load_json(settings.vehicles_per_recharging_node_dict)
	candidates_permits_dict = load_json(settings.candidate_permits_dict)
	fleet_travel_times = load_json(settings.fleet_travel_times)
	traffic_travel_times = load_json(settings.traffic_travel_times)
	traffic = load_json(settings.traffic_demand)
	traffic_nodes = list(traffic.keys())
	traffic_intensity = {i: floor(int(traffic[i]) * settings.percentage_of_evs * settings.percentage_of_vehicles_needing_recharge) for i
						 in list(traffic.keys())}
	rho_list = load_json(settings.rhos)
	zones = load_json(settings.zones)
	zone_bounds = load_json(settings.zone_bounds)
	service_rate = {'candidates': dict(), 'existing': dict()}
	for candidate_node in candidates:
		service_rate['candidates'][candidate_node] = settings.candidate_service_rate
	for existing_node in existing:
		service_rate['existing'][existing_node] = settings.existing_service_rate
	land_cost = dict()
	for candidate_node in candidates:
		if candidate_node not in land_cost:
			land_cost[candidate_node] = float(candidates_permits_dict[str(candidate_node)])


	# #################### REDUCING INPUT SIZE ############################
	reduced_number_of_traffic_nodes =  floor(len(traffic_nodes) * 0.2)
	reduced_number_of_recharging_nodes = floor(len(recharging_nodes) * 1)
	reduced_existing_stations = floor(len(existing) * 1)


	parameters['candidates'] = [i for i in candidates if str(i) in list(candidates_zoning.keys())]
	parameters['existing'] = [i for i in existing[:reduced_existing_stations] if str(i) in list(existing_zoning.keys())]
	parameters['existing_capacities'] = existing_capacities
	parameters['existing_dict'] = existing_stations_dict
	parameters['recharging_nodes'] = recharging_nodes[:reduced_number_of_recharging_nodes]
	parameters['vehicles_per_recharging_node_dict'] = vehicles_per_recharging_node_dict
	parameters['fleet_travel_times'] = fleet_travel_times
	parameters['traffic_travel_times'] = traffic_travel_times
	parameters['traffic_nodes'] = traffic_nodes[:reduced_number_of_traffic_nodes]
	parameters['traffic_intensity'] = traffic_intensity
	parameters['service_rate'] = service_rate
	parameters['fleet_intensity'] = [1 for _ in range(len(recharging_nodes))]
	parameters['land_cost'] = land_cost
	parameters['building_cost'] = settings.charger_building_cost
	parameters['park_and_charge_cost'] = settings.annual_park_and_charge_cost
	parameters['candidates_zoning'] = candidates_zoning
	parameters['zones'] = zones
	parameters['zone_bound'] = zone_bounds
	parameters['rho'] = [float(i) for i in rho_list]
	print('Loaded parameters')
	return parameters


def solve_ilp():
	start_time = time.time()
	prob = LpProblem("problem", pulp.LpMinimize)
	# ################### DATA ####################

	parameters = load_ilp_parameters()
	# variable_space = 'Continuous'
	variable_space = 'Integer'
	b_c = settings.charger_building_cost
	pi_c = settings.annual_park_and_charge_cost

	# ############# Sets, Arrays, Matrices and Dictionaries #################
	n_candidates = len(parameters['candidates'])
	n_existing = len(parameters['existing'])
	n_recharging_nodes = len(parameters['recharging_nodes'])
	n_zones = len(parameters['zones'])
	n_traffic_nodes = len(parameters['traffic_nodes'])
	recharging_nodes_matching_dict = {i: recharging_node for i, recharging_node in enumerate(parameters['recharging_nodes'])}
	traffic_nodes_matching_dict = {i: traffic_node for i, traffic_node in enumerate(parameters['traffic_nodes'])}
	candidates_matching_dict = {i: candidate for i, candidate in enumerate(parameters['candidates'])}
	existing_matching_dict = {i: existing for i, existing in enumerate(parameters['existing'])}
	zone_matching_dict = {i: zone for i, zone in enumerate(parameters['zones'])}

	C_C = [('C_C' + str(j)) for j in range(n_candidates)]
	C_E = [('C_E' + str(j)) for j in range(n_existing)]
	C = C_C + C_E

	C_E_matching_dict = {str(existing): C_E[i] for i, existing in enumerate(parameters['existing'])}

	R = [[]] * n_recharging_nodes
	for i in range(n_recharging_nodes):
		vehicles_per_recharging_node = parameters['vehicles_per_recharging_node_dict'][str(recharging_nodes_matching_dict[i])]
		R[i] = [('R' + str(i)) + '_' + str(j) for j in range(vehicles_per_recharging_node)]
	F = [[]] * n_traffic_nodes
	for i in range(n_traffic_nodes):
		vehicles_per_traffic_node = parameters['traffic_intensity'][str(traffic_nodes_matching_dict[i])]
		F[i] = [('F' + str(i)) + '_' + str(j) for j in range(vehicles_per_traffic_node)]
	V_R = [('R' + str(i)) + '_' + str(j) for i in range(n_recharging_nodes) for j in
		 range(parameters['vehicles_per_recharging_node_dict'][str(recharging_nodes_matching_dict[i])])]
	V_F = [('F' + str(i)) + '_' + str(j) for i in range(n_traffic_nodes) for j in
		 range(parameters['traffic_intensity'][str(traffic_nodes_matching_dict[i])])]
	V = V_R + V_F

	K = [('K' + str(k)) for k in range(settings.max_chargers)]

	K_E = dict()
	for existing_id, existing_capacity in parameters['existing_capacities'].items():
		if int(existing_id) in parameters['existing']:
			K_E[C_E_matching_dict[existing_id]] = existing_capacity		# existing CSs capacities

	H = [('H' + str(n)) for n in range(n_zones)]

	t = dict()
	for i in range(n_recharging_nodes):
		recharging_node_name = 'R' + str(i)
		recharging_node_index = str(recharging_nodes_matching_dict[i])
		t[recharging_node_name] = dict()
		for j, candidate in enumerate(C_C):
			candidate_id = str(parameters['candidates'][j])
			t[recharging_node_name][candidate] = parameters['fleet_travel_times'][recharging_node_index][candidate_id]
		for j, existing in enumerate(C_E):
			existing_id = str(parameters['existing'][j])
			t[recharging_node_name][existing] = parameters['fleet_travel_times'][recharging_node_index][existing_id]
	for i in range(n_traffic_nodes):
		traffic_node_name = 'F' + str(i)
		traffic_node_index = str(traffic_nodes_matching_dict[i])
		t[traffic_node_name] = dict()
		for j, existing in enumerate(C_E):
			existing_id = str(parameters['existing'][j])
			t[traffic_node_name][existing] = parameters['traffic_travel_times'][traffic_node_index][existing_id]

	in_zone = dict()
	for n, zone in enumerate(H):
		zone_id = parameters['zones'][n]
		in_zone[zone] = dict()
		for j, candidate in enumerate(C_C):
			candidate_id = str(parameters['candidates'][j])
			if parameters['candidates_zoning'][candidate_id] == zone_id:
				in_zone[zone][candidate] = 1
			else:
				in_zone[zone][candidate] = 0
	# p = {candidate:parameters['existing'][j] for j, candidate in enumerate(C)}
	l_c = {candidate:parameters['land_cost'][candidates_matching_dict[j]] for j, candidate in enumerate(C_C)}
	# f_i = {vehicle:parameters['fleet_intensity'][i] for i, vehicle in enumerate(R)}
	# t_i = {traffic_node:parameters['traffic_intensity'][j] for j, traffic_node in enumerate(F)}
	rho = {charger:parameters['rho'][m] for m, charger in enumerate(K)}
	mu = {candidate: parameters['service_rate']['candidates'][candidates_matching_dict[j]] for j, candidate
					 in enumerate(C_C)}
	mu.update({existing: parameters['service_rate']['existing'][existing_matching_dict[j]] for j, existing
					 in enumerate(C_E)})
	# mu = dict(mu_candidates.items() + mu_existing.items())
	upper_bound = {zone:parameters['zone_bound'][str(zone_matching_dict[n])] for n, zone in enumerate(H)}
	print('Loaded problem parameters')

	# #################### Variables ###################################
	x = LpVariable.dicts('x', (V,C), lowBound=0, upBound=1, cat=variable_space)
	y = LpVariable.dicts('y', C, lowBound=0, upBound=1, cat=variable_space)
	omega = LpVariable.dicts('omega', C, lowBound=0, upBound=1, cat=variable_space)
	# psi = LpVariable.dicts('psi', C, lowBound=0, upBound=max_chargers, cat=variable_space)
	z = LpVariable.dicts('z', (C,K), lowBound=0, upBound=1, cat=variable_space)

	# ################ Linearisation variables ##########################
	w = LpVariable.dicts('w', C, lowBound=0, upBound=1, cat=variable_space)
	theta = LpVariable.dicts('theta', (C,K), lowBound=0, upBound=1, cat=variable_space)
	u = LpVariable.dicts('u', (V_F, C_E), lowBound=0, upBound=1, cat=variable_space)

	print('Loaded variables')
	# ##################### Objective ################################
	T = lpSum([lpSum([t[i.split('_')[0]][j] * x[i][j]] for j in C)] for i in V_R) + \
		lpSum([lpSum([t[i.split('_')[0]][j] * x[i][j]] for j in C_E)] for i in V_F)

	total_land_cost = lpSum( [l_c[j] * y[j]] for j in C_C)

	total_infrastructure_cost = lpSum(b_c * lpSum([z[j][m]] for m in K) for j in C_C)

	total_park_and_charge_cost = lpSum( [pi_c * lpSum([x[i][j]] for i in V_R)] for j in C_E)

	M = total_land_cost + total_infrastructure_cost + total_park_and_charge_cost

	prob += settings.q_time_to_monetary_units * T + M

	# ##################### Constraints ################################
	# Constraint (11)
	for i in V_F:
		prob += lpSum([x[i][j] - u[i][j]] for j in C_E) == 1

	# Constraint (12)
	for i in V_R:
		prob += lpSum( [x[i][j]] for j in C) == 1

	# Constraint (13)
	for i in V_R:
		for j in C:
			prob += x[i][j] <= y[j]

	for i in V_F:
		for j in C_E:
			prob += x[i][j] <= y[j]

	# Constraint (14)
	for j in C_C:
		prob += lpSum([x[i][j]] for i in V_R) <= lpSum([z[j][m]] for m in K)

	# Constraint (15)
	for j in C_E:
		prob += lpSum([x[i][j]] for i in V) <= K_E[j]

	# Constraint (16)
	for j in C_C:
		for index, m in enumerate(K[1:]):
			prob += z[j][K[index + 1]] <= z[j][K[index]]

	# Constraint (17)
	for j in C_C:
		prob += lpSum([x[i][j]] for i in V_R) <= mu[j] * (z[j]['K0'] * rho['K0'] +
				lpSum([z[j][m] * (rho['K' + str(index + 1)] - rho['K' + str(index)])] for index, m in enumerate(K[1:])))

	# Constraint (18)
	for j in C_E:
		prob += lpSum([x[i][j]] for i in V) <= mu[j] * (rho['K0'] +
				lpSum([(rho['K' + str(index + 1)] - rho['K' + str(index)])] for index, m in enumerate(K[1:])))

	# Constraint (19)
	for n in H:
		prob += lpSum( [y[j] - w[j]] for j in C_C if in_zone[n][j]) <= upper_bound[n]

	# ################ Linearisation constraints #######################

	# Constraints (22-30)
	for j in C_C:
		prob += w[j] <= y[j]
		prob += w[j] <= omega[j]
		prob += w[j] >= y[j] + omega[j] - 1
	for j in C_E:
		for i in V_F:
			prob += u[i][j] <= x[i][j]
			prob += u[i][j] <= omega[j]
			prob += u[i][j] >= x[i][j] + omega[j] - 1
	for j in C:
		for m in K:
			prob += theta[j][m] <= z[j][m]
			prob += theta[j][m] <= omega[j]
			prob += theta[j][m] >= z[j][m] + omega[j] - 1

	print('Loaded constraints and objective')
	save_formulation(prob)
	print('Solving the problem ...')
	status = prob.solve()
	print(LpStatus[status])
	# print(prob)

	running_time = time.time() - start_time
	solution_dict = dict()
	solution_dict['feasibility'] = 'feasible' if status == 1 else '************ INFEASIBLE **************'
	solution_dict['running_time_in_seconds'] = running_time
	solution_dict['n_candidates'] = settings.centroids
	solution_dict['n_existing'] = n_existing
	solution_dict['traffic_vehicles'] = len(V_F)
	solution_dict['TNC_vehicles'] = len(V_R)
	solution_dict['percentage_of_evs'] = settings.percentage_of_evs
	solution_dict['percentage_of_vehicles_needing_recharge'] = settings.percentage_of_vehicles_needing_recharge
	solution_dict['objective'] = value(prob.objective)
	for v in prob.variables():
		solution_dict[v.name] = v.varValue
	save_solution(solution_dict, variable_space)


def solve_optimal():
	solve_ilp()