# LIBRARIES
from __future__ import division
import pyomo.opt
from pyomo.environ import *
# FILES
import settings
import i_o.serializationIO as serializationIO


def invertDict(originalDict):
	return {v: k for k, v in originalDict.items()}


def optimalModel():
	model = AbstractModel()
	infinity = float('inf')

	# ### SETS ###
	# Facilities
	model.F = Set()
	# Vehicles
	model.V = Set()


	# ### PARAMETERS ###
	# Travelling time from vehicle i to facility j
	model.t = Param(model.V, model.F, within=PositiveReals, default=infinity)
	# Maximum number of facilities to open
	model.k = Param(within=PositiveIntegers)


	# ### VARIABLES ###
	# Indicator of whether vehicle i connects to facility j
	model.x = Var(model.V, model.F, domain=Binary, initialize=0)
	# Indicator of whether facility j is open or not
	model.y = Var(model.F, domain=Binary, initialize=0)


	# ### OBJECTIVE ###
	# Minimize the total travelling time
	def total_time(model):
		return sum(model.t[i,j] * model.x[i,j] for i in model.V for j in model.F)
		# return sum(model.x[i,j] for i in model.V for j in model.F)
	model.time = Objective(rule=total_time, sense=minimize)


	# ### CONSTRAINTS ###
	def bound_on_open_facilities(model):
		return sum(model.y[j] for j in model.F) <= model.k
	model.facilitiesBound = Constraint(rule=bound_on_open_facilities)

	def vehicle_connection_to_at_least_one_facility(model, i):
		return sum(model.x[i,j] for j in model.F) >= 1
	model.vehicleConnectionToFacility = Constraint(model.V, rule=vehicle_connection_to_at_least_one_facility)

	def facility_open_if_vehicle_is_connected(model, i, j):
		return model.y[j] >= model.x[i,j]
	model.openIfConnectionExists = Constraint(model.V, model.F, rule=facility_open_if_vehicle_is_connected)
	return model




def optimal():
	S = []
	model = optimalModel()
	instance = model.create_instance(settings.optimalDataFile)
	# instance.display()
	opt = pyomo.opt.SolverFactory("glpk")
	results=opt.solve(instance)
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

	optimalMapping = serializationIO.importAndDeserialize(settings.optimalMapping)
	invertedMapping = invertDict(optimalMapping)
	for j in range(len(instance.F)):
		if value(instance.y[j+1]) == 1:
			S.append(invertedMapping[str(j+1)])
	return S, value(instance.time)
