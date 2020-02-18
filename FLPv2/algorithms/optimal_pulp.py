from pulp import *

prob = LpProblem("problem", pulp.LpMinimize)


# ################### DATA ####################
n_chargers = 10
r = 1
candidates = [1,2,3]
traffic_intensity = [1,0,0]
service_rate = [1,2,3]
recharging_nodes = [1,2,3]
fleet_intensity = [0,1,0]
zones = [1,2,3,4]
traveling_times = [[0,1,2],[4,8,9],[1,7,5]]
existing = [0,0,0]
land_cost = [10,20,30]
building_cost = [100,200,300]
park_and_charge_cost = [0.5,0.6,0.7]
rho_fraction = [1,2,3,4,5,6,7,8,9,10]
zone_upper_bound = [10,12,15,14]
candidate_in_zone = [[0,0,1], [0,0,0],[1,0,0],[0,1,0]]


# ############# Sets, Arrays, Matrices and Dictionaries #################
n_candidates = len(candidates)
n_recharging_nodes = len(recharging_nodes)
n_zones = len(zones)

C = [('C' + str(j+1)) for j in range(n_candidates)]
R = [('R' + str(i+1)) for i in range(n_recharging_nodes)]
H = [('H' + str(n+1)) for n in range(n_zones)]
K = [('K' + str(n+1)) for n in range(n_chargers)]


t = {vehicle:{candidate:traveling_times[i][j] for j, candidate in enumerate(C)} for i, vehicle in enumerate(R)}
p = {candidate:existing[j] for j, candidate in enumerate(C)}
l_c = {candidate:land_cost[j] for j, candidate in enumerate(C)}
b_c = {candidate:building_cost[j] for j, candidate in enumerate(C)}
pi_c = {candidate:park_and_charge_cost[j] for j, candidate in enumerate(C)}
f_i = {vehicle:fleet_intensity[i] for i, vehicle in enumerate(R)}
t_i = {candidate:traffic_intensity[j] for j, candidate in enumerate(C)}
rho = {charger:rho_fraction[m] for m, charger in enumerate(K)}
mu = {candidate:service_rate[j] for j, candidate in enumerate(C)}
in_zone = {zone:{candidate:candidate_in_zone[n][j] for j, candidate in enumerate(C)} for n, zone in enumerate(H)}
upper_bound = {zone:zone_upper_bound[n] for n, zone in enumerate(H)}


# #################### Variables ###################################
x = LpVariable.dicts('x', (R,C), lowBound=0, upBound=1, cat=LpInteger)
y = LpVariable.dicts('y', C, lowBound=0, upBound=1, cat=LpInteger)
omega = LpVariable.dicts('omega', C, lowBound=0, upBound=1, cat=LpInteger)
psi = LpVariable.dicts('psi', C, lowBound=0, upBound=n_chargers, cat=LpInteger)
z = LpVariable.dicts('z', (C,K), lowBound=0, upBound=1, cat=LpInteger)

# ################ Linearisation variables ##########################
# w_j = y_j * omega_j
w = LpVariable.dicts('w', C, lowBound=0, upBound=1, cat=LpInteger)
# theta_j = z_{jm} * omega_j
theta = LpVariable.dicts('theta', (C,K), lowBound=0, upBound=1, cat=LpInteger)

# ##################### Objective ################################
T = lpSum( [lpSum( [t[i][j] * x[i][j]] for j in C )] for i in R)

total_land_cost = lpSum( [(1-p[j]) * l_c[j] * w[j]] for j in C)

total_infrastructure_cost = lpSum( [(1-p[j]) * b_c[j] * lpSum([theta[j][m]] for m in K)] for j in C)

total_park_and_charge_cost = lpSum( [pi_c[j] * psi[j] - pi_c[j] * lpSum([theta[j][m]] for m in K)] for j in C)

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
# for v in prob.variables():
# 	print(v.name, "=", v.varValue)