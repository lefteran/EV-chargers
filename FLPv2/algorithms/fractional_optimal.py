# LIBRARIES
from __future__ import division
import pyomo.opt
import json
from pyomo.environ import *
# FILES
import settings


def invert_dict(originalDict):
	return {v: k for k, v in originalDict.items()}


def optimalModel():
	model = AbstractModel()
	infinity = float('inf')

	# ### SETS ###
	# Candidate locations
	model.C = Set()
	# Vehicles
	model.V = Set()


	# ### PARAMETERS ###
	# Travelling time from vehicle i to location j
	model.t = Param(model.V, model.C, within=NonNegativeReals, default=0)
	# Maximum number of facilities to open
	model.k = Param(within=PositiveIntegers)


	# ### VARIABLES ###
	# Indicator of whether vehicle i connects to location j
	model.x = Var(model.V, model.C, within=NonNegativeReals, initialize=0)
	# Indicator of whether facility at location j is open or not
	model.y = Var(model.C, within=NonNegativeReals, initialize=0)


	# ### OBJECTIVE ###
	# Minimize the total travelling time
	def total_time(model):
		return sum(model.t[i,j] * model.x[i,j] for i in model.V for j in model.C)
		# return sum(model.x[i,j] for i in model.V for j in model.C)
	model.time = Objective(rule=total_time, sense=minimize)


	# ### CONSTRAINTS ###
	def bound_on_open_facilities(model):
		return sum(model.y[j] for j in model.C) <= model.k
	model.facilitiesBound = Constraint(rule=bound_on_open_facilities)

	def vehicle_connection_to_at_least_one_facility(model, i):
		return sum(model.x[i,j] for j in model.C) >= 1
	model.vehicleConnectionToFacility = Constraint(model.V, rule=vehicle_connection_to_at_least_one_facility)

	def facility_open_if_vehicle_is_connected(model, i, j):
		return model.y[j] >= model.x[i,j]
	model.openIfConnectionExists = Constraint(model.V, model.C, rule=facility_open_if_vehicle_is_connected)
	return model




def fractional_optimal():
	S = []
	model = optimalModel()
	instance = model.create_instance(settings.optimal_dat_file)
	# instance.display()
	opt = pyomo.opt.SolverFactory("glpk")
	results = opt.solve(instance)
	# instance.solutions.store_to(results)
	# print(results)
	if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
		print("\nfeasible")
	else:
		print("\ninfeasible")

	# print("\nObjective is: ", value(instance.time))
	#
	# print("\ny: ")
	# for j in range(len(instance.F)):
	# 	print(value(instance.y[j+1]))
	# print("\nx:")
	# for i in range(len(instance.V)):
	# 	for j in range(len(instance.F)):
	# 		print(value(instance.x[i+1, j + 1]))

	optimal_mapping = load_mapping()
	inverted_mapping = invert_dict(optimal_mapping)
	for j in range(len(instance.C)):
		if value(instance.y[j+1]) == 1:
			S.append(inverted_mapping[j+1])
	return S, value(instance.time)



def load_mapping():
	with open(settings.mapping_for_optimal, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict