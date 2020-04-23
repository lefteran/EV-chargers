# LIBRARIES
import json
from math import factorial
from sympy.solvers import solve
from sympy import Symbol
# FILES
import settings


def save_rhos(list_to_be_saved):
	filename = settings.rhos
	json_file = json.dumps(list_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


def compute_rho(m, a, b, rho_list):
	rho = Symbol('rho', real = True, positive = True)
	nominator = 0
	denominator = 0
	constant_term = 1 / (1 - a)
	for k in range(m):
		nominator += (m-k) * factorial(m) * m**b
		denominator += factorial(k) * rho ** (m+b+1-k)
	equation = nominator / denominator - constant_term
	res = solve(equation, rho)
	if res:
		rho_list.append(str(res[0]))
	return rho_list


def compute_rho_list():
	rho_list = list()
	for n_chargers in range(settings.max_chargers):
		compute_rho(n_chargers+1, settings.alpha_probability, settings.b_vehicles_in_queue, rho_list)
	save_rhos(rho_list)