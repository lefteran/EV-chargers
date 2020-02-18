# LIBRARIES
from __future__ import division
import json
import pyomo.opt
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
	# Chargers
	model.N = Set()


	# ### PARAMETERS ###
	# Travelling time from vehicle i to location j
	model.t = Param(model.V, model.C, within=NonNegativeReals, default=0)
	# lambda parameter
	model.time_to_money = Param(within=PositiveReals)
	# Maximum number of on-street chargers per facility
	model.N_ON = Param(within=PositiveIntegers)
	# Maximum number of off-street chargers per facility
	model.N_OFF = Param(within=PositiveIntegers)
	# Indicator of whether a facility already exists or not
	model.p = Param(model.C, within=PositiveIntegers)
	# Land, building and maintenance cost
	model.c = Param(model.C, within=PositiveReals)
	# Charging time
	model.tau = Param(within=PositiveReals)
	# Number of chargers of pre-existing CSs
	model.n = Param(model.C, within=PositiveReals)



	# ### VARIABLES ###
	# Indicator of whether vehicle i is assigned to CS at location j
	model.x = Var(model.V, model.C, domain=Binary, initialize=0)
	# Indicator of whether the CS at location j is built or not
	model.y = Var(model.C, domain=Binary, initialize=0)
	# Indicator of whether the CS at location j (if built) is on/off-street
	model.omega = Var(model.C, domain=Binary, initialize=0)
	# Indicator of the number of chargers of CS at location j
	model.psi = Var(model.C, domain=Integers, initialize=0)

	# ------ LINEARISATION VARIABLES ----------
	# Integer binarisation
	model.z = Var(model.C, model.N, domain=Binary, initialize=0)
	# Product simplification
	model.w = Var(model.C, model.N, domain=Binary, initialize=0)




	# ### OBJECTIVE ###
	# Minimize the total travelling time
	def total_time_and_money(model):
		return model.time_to_money * sum(model.t[i, j] * model.x[i, j] for i in model.V for j in model.C) + sum(model.c[j] * model.y[j] for j in model.C)
	model.time_and_money = Objective(rule=total_time_and_money, sense=minimize)


	# ### CONSTRAINTS ###

	def vehicle_assignment_to_exactly_one_facility(model, i):
		return sum(model.x[i,j] for j in model.C) == 1
	model.vehicleAssignmentToFacility = Constraint(model.V, rule=vehicle_assignment_to_exactly_one_facility)

	def facility_open_if_vehicle_assigned(model, i, j):
		return model.y[j] >= model.x[i,j]
	model.openIfAssignmentExists = Constraint(model.V, model.C, rule=facility_open_if_vehicle_assigned)

	def facility_open_if_it_exists(model, j):
		return model.p[j] <= model.y[j]
	model.openIfFacilityExists = Constraint(model.C, rule=facility_open_if_it_exists)

	def chargers_bound(model, j):
		return model.psi[j] <= model.N_ON - model.N_ON * model.omega[j] + model.N_OFF * model.omega[j]
	model.bound_on_number_of_chargers = Constraint(model.C, rule=chargers_bound)

	def capacity_constraint(model, j):
		return sum(model.x[i,j] for i in model.V) <= (24 / model.tau) * (model.n[j] * model.p[j] + model.psi[j] - model.p[j] * model.psi[j])
	model.capacityConstraint = Constraint(model.C, rule=capacity_constraint)

	# ------ LINEARISATION CONSTRAINTS ----------

	def linearisation_eq_1(model, j):
		return sum(model.z[j,k] for k in model.N) == 1
	model.linearisationEq1 = Constraint(model.C, rule=linearisation_eq_1)

	def linearisation_eq_2(model, j):
		return model.psi[j] == sum(k * model.z[j,k] for k in model.N)
	model.linearisationEq2 = Constraint(model.C, rule=linearisation_eq_2)

	def product_constraint_1(model, j, k):
		return - model.z[j,k] + model.w[j,k] <= 0
	model.productConstraint1 = Constraint(model.C, model.N, rule=product_constraint_1)

	def product_constraint_2(model, j, k):
		return - model.y[j] + model.w[j,k] <= 0
	model.productConstraint2 = Constraint(model.C, model.N, rule=product_constraint_2)

	def product_constraint_3(model, j, k):
		return model.z[j,k] + model.y[j] - model.w[j,k] <= 1
	model.productConstraint3 = Constraint(model.C, model.N, rule=product_constraint_3)

	return model




def integer_optimal():
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