# LIBRARIES
from pulp import *
import json
from random import randint
from math import floor
# FILES
import settings

def load_json(filename):
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict


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


	parameters['candidates_zoning'] = candidates_zoning
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
	parameters['service_rate'] = service_rate
	parameters['fleet_intensity'] = [1 for _ in range(len(recharging_nodes))]
	parameters['land_cost'] = land_cost
	parameters['building_cost'] = settings.charger_building_cost
	parameters['park_and_charge_cost'] = settings.annual_park_and_charge_cost
	parameters['zone_bound'] = zone_bounds
	parameters['rho'] = [float(i) for i in rho_list]
	parameters['zones'] = zones
	return parameters


def solve_ilp():
	prob = LpProblem("problem", pulp.LpMinimize)
	# ################### DATA ####################

	parameters = load_ilp_parameters()
	variable_space = 'Continuous'
	# variable_space = 'Integer'
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

	C_c = [('C_c' + str(j)) for j in range(n_candidates)]
	C_e = [('C_e' + str(j)) for j in range(n_existing)]
	C = C_c + C_e

	R = [[]] * n_recharging_nodes
	for i in range(n_recharging_nodes):
		vehicles_per_recharging_node = parameters['vehicles_per_recharging_node_dict'][str(recharging_nodes_matching_dict[i])]
		R[i] = [('R' + str(i)) + '_' + str(j) for j in range(vehicles_per_recharging_node)]
	F = [[]] * n_traffic_nodes
	for i in range(n_traffic_nodes):
		vehicles_per_traffic_node = parameters['traffic_intensity'][str(traffic_nodes_matching_dict[i])]
		F[i] = [('F' + str(i)) + '_' + str(j) for j in range(vehicles_per_traffic_node)]
	# R = [('R' + str(i + 1)) + '_' + str(j + 1) for i in range(n_recharging_nodes) for j in
	# 	 range(parameters['vehicles_per_recharging_node_dict'][str(recharging_nodes_matching_dict[i + 1])])]
	# F = [('F' + str(i + 1)) + '_' + str(j + 1) for i in range(n_traffic_nodes) for j in
	# 	 range(parameters['traffic_intensity'][str(traffic_nodes_matching_dict[i + 1])])]
	V = R + F

	K = [('K' + str(k)) for k in range(settings.max_chargers)]
	H = [('H' + str(n)) for n in range(n_zones)]

	t = dict()
	for i in range(n_recharging_nodes):
		recharging_node_name = 'R' + str(i)
		recharging_node_index = str(recharging_nodes_matching_dict[i])
		t[recharging_node_index] = dict()
		for j, candidate in enumerate(C_c):
			candidate_id = str(parameters['candidates'][j])
			t[recharging_node_name][candidate] = parameters['fleet_travel_times'][recharging_node_index][candidate_id]
		for j, existing in enumerate(C_e):
			existing_id = str(parameters['existing'][j])
			t[recharging_node_index][existing] = parameters['fleet_travel_times'][recharging_node_index][existing_id]
	for i in range(n_traffic_nodes):
		traffic_node_id = str(parameters['traffic_nodes'][i])
		t[vehicle] = dict()
		for j, candidate in enumerate(C):
			candidate_id = str(parameters['candidates'][j])
			t[vehicle][candidate] = parameters['traffic_travel_times'][traffic_node_id][candidate_id]

	in_zone = dict()
	for n, zone in enumerate(H):
		zone_id = parameters['zones'][n]
		in_zone[zone] = dict()
		for j, candidate in enumerate(C):
			candidate_id = str(parameters['candidates'][j])
			if parameters['contained'][candidate_id] == zone_id:
				in_zone[zone][candidate] = 1
			else:
				in_zone[zone][candidate] = 0
	p = {candidate:parameters['existing'][j] for j, candidate in enumerate(C)}
	l_c = {candidate:parameters['land_cost'][j] for j, candidate in enumerate(C)}
	f_i = {vehicle:parameters['fleet_intensity'][i] for i, vehicle in enumerate(R)}
	t_i = {traffic_node:parameters['traffic_intensity'][j] for j, traffic_node in enumerate(F)}
	rho = {charger:parameters['rho'][m] for m, charger in enumerate(K)}
	mu = {candidate:parameters['service_rate'][j] for j, candidate in enumerate(C)}
	upper_bound = {zone:parameters['zone_upper_bound'][n] for n, zone in enumerate(H)}


	# #################### Variables ###################################
	x = LpVariable.dicts('x', (V,C), lowBound=0, upBound=1, cat=variable_space)
	y = LpVariable.dicts('y', C, lowBound=0, upBound=1, cat=variable_space)
	omega = LpVariable.dicts('omega', C, lowBound=0, upBound=1, cat=variable_space)
	# psi = LpVariable.dicts('psi', C, lowBound=0, upBound=max_chargers, cat=variable_space)
	z = LpVariable.dicts('z', (C,K), lowBound=0, upBound=1, cat=variable_space)

	# ################ Linearisation variables ##########################
	w = LpVariable.dicts('w', C, lowBound=0, upBound=1, cat=variable_space)
	theta = LpVariable.dicts('theta', (C,K), lowBound=0, upBound=1, cat=variable_space)
	u = LpVariable.dicts('u', (F, C), lowBound=0, upBound=1, cat=variable_space)

	# ##################### Objective ################################
	T = lpSum( [lpSum( [t[i][j] * x[i][j]] for j in C )] for i in V)

	total_land_cost = lpSum( [(1-p[j]) * l_c[j] * w[j]] for j in C)

	total_infrastructure_cost = lpSum( [(1-p[j]) * b_c * lpSum([theta[j][m]] for m in K)] for j in C)

	total_park_and_charge_cost = lpSum( [pi_c * psi[j] - pi_c * lpSum([theta[j][m]] for m in K)] for j in C)

	M = total_land_cost + total_infrastructure_cost + total_park_and_charge_cost

	prob += settings.q_time_to_monetary_units * T + M

	# ##################### Constraints ################################
	for i in R:
		prob += lpSum( [x[i][j]] for j in C) == 1

	for j in C:
		for i in V:
			prob += x[i][j] <= y[j]
			prob += x[i][j] <= z[j]['K1']
		for m, charger in enumerate(K[1:]):
			prob += z[j][charger] <= z[j]['K' + str(m+1)]
		prob += p[j] <= y[j]
		prob += lpSum([f_i[i] * x[i][j]] for i in R) + lpSum([t_i[i] * x[i][j]] for i in F) <= mu[j] * (z[j]['K1'] * rho['K1'] + lpSum(
			[z[j][charger] * (rho[charger] - rho['K' + str(m + 1)]) for m, charger in enumerate(K[1:])]))

	for n in H:
		prob += lpSum( [ y[j] - w[j]] for j in C if in_zone[n][j]) <= upper_bound[n]

	# ################ Linearisation constraints #######################
	for i in F:
		prob += lpSum( [u[i][j]] for j in C) == 1

	for j in C:
		prob += w[j] <= y[j]
		prob += w[j] <= omega[j]
		prob += w[j] >= y[j] + omega[j] - 1
		for i in F:
			prob += u[i][j] <= x[i][j]
			prob += u[i][j] <= omega[j]
			prob += u[i][j] >= x[i][j] + omega[j] - 1
		for m in K:
			prob += theta[j][m] <= z[j][m]
			prob += theta[j][m] <= omega[j]
			prob += theta[j][m] >= z[j][m] + omega[j] - 1

	status = prob.solve()

	print(LpStatus[status])
	solution_dict = dict()
	solution_dict['objective'] = value(prob.objective)
	for v in prob.variables():
		solution_dict[v.name] = v.varValue
	save_solution(solution_dict, variable_space)


def solve_optimal():
	solve_ilp()