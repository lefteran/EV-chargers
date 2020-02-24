# LIBRARIES
from pulp import *
import json
from random import randint
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
	hour = '1'
	candidates = load_json(settings.candidates_and_existing)
	existing_station_ids = load_json(settings.existing_stations_closest_nodes)
	recharging_nodes_per_hour = load_json(settings.recharging_nodes_per_hour)
	recharging_nodes = recharging_nodes_per_hour[hour]
	travel_times_per_hour = load_json(settings.travel_times_per_hour)
	travel_times = travel_times_per_hour[hour]
	existing = list()
	for _ in candidates:
		if candidates in list(existing_station_ids.values()):
			existing.append(1)
		else:
			existing.append(0)
	rho_list = load_json(settings.rhos)
	zones = load_json(settings.zones)
	contained = load_json(settings.contained_in_zone)

	parameters['contained'] = contained
	parameters['candidates'] = [i for i in candidates if i in contained]
	parameters['recharging_nodes'] = recharging_nodes
	parameters['travel_times'] = travel_times
	parameters['traffic_intensity'] = [randint(0,20) for _ in range(len(candidates))]
	parameters['service_rate'] = [randint(1, 3) for _ in range(len(candidates))]
	parameters['fleet_intensity'] = [randint(0, 20) for _ in range(len(recharging_nodes))]
	parameters['land_cost'] = [randint(100, 300) for _ in range(len(candidates))]
	parameters['building_cost'] = [randint(100, 300)]
	parameters['park_and_charge_cost'] = [randint(10, 50)]
	parameters['zone_upper_bound'] = [randint(5, 15) for _ in range(len(zones))]
	parameters['existing'] = existing
	parameters['rho'] = [float(i) for i in rho_list]
	parameters['zones'] = zones
	return parameters


def solve_ilp():
	prob = LpProblem("problem", pulp.LpMinimize)
	# ################### DATA ####################

	parameters = load_ilp_parameters()
	# variable_space = 'Continuous'
	variable_space = 'Integer'
	max_chargers = 15
	b_c = 100
	pi_c = 0.8
	r = 1

	# ############# Sets, Arrays, Matrices and Dictionaries #################
	n_candidates = len(parameters['candidates'])
	n_recharging_nodes = len(parameters['recharging_nodes'])
	n_zones = len(parameters['zones'])

	C = [('C' + str(j+1)) for j in range(n_candidates)]
	R = [('R' + str(i+1)) for i in range(n_recharging_nodes)]
	H = [('H' + str(n+1)) for n in range(n_zones)]
	K = [('K' + str(k+1)) for k in range(max_chargers)]

	t = dict()
	for i, vehicle in enumerate(R):
		recharging_node_id = str(parameters['recharging_nodes'][i])
		t[vehicle] = dict()
		for j, candidate in enumerate(C):
			candidate_id = str(parameters['candidates'][j])
			t[vehicle][candidate] = parameters['travel_times'][recharging_node_id][candidate_id]

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
	t_i = {candidate:parameters['traffic_intensity'][j] for j, candidate in enumerate(C)}
	rho = {charger:parameters['rho'][m] for m, charger in enumerate(K)}
	mu = {candidate:parameters['service_rate'][j] for j, candidate in enumerate(C)}
	upper_bound = {zone:parameters['zone_upper_bound'][n] for n, zone in enumerate(H)}


	# #################### Variables ###################################
	x = LpVariable.dicts('x', (R,C), lowBound=0, upBound=1, cat=variable_space)
	y = LpVariable.dicts('y', C, lowBound=0, upBound=1, cat=variable_space)
	omega = LpVariable.dicts('omega', C, lowBound=0, upBound=1, cat=variable_space)
	psi = LpVariable.dicts('psi', C, lowBound=0, upBound=max_chargers, cat=variable_space)
	z = LpVariable.dicts('z', (C,K), lowBound=0, upBound=1, cat=variable_space)

	# ################ Linearisation variables ##########################
	# w_j = y_j * omega_j
	w = LpVariable.dicts('w', C, lowBound=0, upBound=1, cat=variable_space)
	# theta_j = z_{jm} * omega_j
	theta = LpVariable.dicts('theta', (C,K), lowBound=0, upBound=1, cat=variable_space)

	# ##################### Objective ################################
	T = lpSum( [lpSum( [t[i][j] * x[i][j]] for j in C )] for i in R)

	total_land_cost = lpSum( [(1-p[j]) * l_c[j] * w[j]] for j in C)

	total_infrastructure_cost = lpSum( [(1-p[j]) * b_c * lpSum([theta[j][m]] for m in K)] for j in C)

	total_park_and_charge_cost = lpSum( [pi_c * psi[j] - pi_c * lpSum([theta[j][m]] for m in K)] for j in C)

	M = total_land_cost + total_infrastructure_cost + total_park_and_charge_cost

	prob += r * T + M

	# ##################### Constraints ################################
	for i in R:
		prob += lpSum( [x[i][j]] for j in C) == 1

	for j in C:
		for i in R:
			prob += x[i][j] <= y[j]
			prob += x[i][j] <= z[j]['K1']
		for m, charger in enumerate(K[1:]):
			prob += z[j][charger] <= z[j]['K' + str(m+1)]
		prob += p[j] <= y[j]
		prob += lpSum([f_i[i] * x[i][j]] for i in R) + t_i[j] * omega[j] <= mu[j] * (z[j]['K1'] * rho['K1'] + lpSum(
			[z[j][charger] * (rho[charger] - rho['K' + str(m + 1)]) for m, charger in enumerate(K[1:])]))

	for n in H:
		prob += lpSum( [ y[j] - w[j]] for j in C if in_zone[n][j]) <= upper_bound[n]

	# ################ Linearisation constraints #######################
	for j in C:
		prob += w[j] <= y[j]
		prob += w[j] <= omega[j]
		prob += w[j] >= y[j] + omega[j] - 1
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