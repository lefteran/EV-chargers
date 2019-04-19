from __future__ import division
import pyomo.opt 
from pyomo.environ import *
# pyomo solve --solver=glpk example_pyomo.py example-pyomo.dat

model = AbstractModel()

# ### SETS ###
# Facilities
model.F = Set()
# Zones
model.Z = Set()
# Vehicles
model.V = Set()

# ### PARAMETERS ###
# Budget
model.B = Param(within=PositiveIntegers)
# Distance of a vehicle to a facility
model.dist = Param(model.V, model.F, within=PositiveReals)
# Cost of opening a facility
model.c = Param(model.F, within=PositiveReals)
# Cost of installing a CP of standard speed
model.cst = Param(within=PositiveReals)
# Cost of installing a CP of rapid speed
model.cr = Param(within=PositiveReals)
# Capacity of each facility
model.cap = Param(model.F, within=PositiveIntegers)
# Indicator of type (on-off-street)
model.a = Param(model.F, within=Binary, mutable=True)
# Demand of each zone
model.dem = Param(model.Z, within=PositiveIntegers, mutable=True)
# Limit on the number of on-street spaces in zone z
model.Nz = Param(model.Z, within=PositiveIntegers)
# Binary (belonging) matrix denoting whether a facility belongs to a zone
model.H = Param(model.F, model.Z, within=Binary, mutable=True)
# Adjacency matrix denoting whether a zone is adjacent to another
model.A = Param(model.Z, model.Z, within=Binary, mutable=True)
# Minimum number of rapid chargers
model.R = Param(within=PositiveIntegers)
# Proportion of charging demand to be satisfied
model.gamma = Param(within=PositiveReals)



# ### VARIABLES ###
# Number of standard chargers per facility
model.st = Var(model.F, domain=NonNegativeIntegers, initialize=0)
# Number of rapid chargers per facility
model.r = Var(model.F, domain=NonNegativeIntegers, initialize=0)
# Number of total chargers per facility
model.y = Var(model.F, domain=NonNegativeIntegers, initialize=0)
# Indication of whether a station is open or not
model.omega = Var(model.F, domain=Binary, initialize=0)
# Indication of whether a vehicle is connected to a station or not
model.x = Var(model.V, model.F, domain=Binary, initialize=0)



# ### OBJECTIVE ###
# Minimize the overall distance from vehicles to facilities
def cost_rule(model):
	return sum(model.dist[i,j] * model.x[i,j] for i in model.V for j in model.F)
model.cost = Objective(rule=cost_rule)


# ### CONSTRAINTS ###

# Budget constraint
def budget(model):
	return sum(model.c[j] * model.omega[j] + model.cst * model.st[j] + model.cr * model.r[j] for j in model.F) <= model.B
model.budget_constraint = Constraint(rule=budget)

# sum(x_{ij}) >= 1
def connectivity(model, i):
	return sum(model.x[i,j] for j in model.F) >= 1
model.connectivity_constraint = Constraint(model.V, rule=connectivity)

# omega_j >= x_{ij}
def open_station(model, i, j):
	return model.omega[j] >= model.x[i,j]
model.open_station_constraint = Constraint(model.V, model.F, rule=open_station)

# y_j >= omega_j
def chargers_number(model, j):
	return model.y[j] >= model.omega[j]
model.chargers_number_constraint = Constraint(model.F, rule=chargers_number)

# rapid chargers 
def rapid_chargers(model):
	return sum(model.r[j] for j in model.F) >= model.R
model.rapid_chargers_bound = Constraint(rule=rapid_chargers)

# y_j = y_j^{st} + y_j^r
def total_chargers(model, j):
	return model.y[j] == model.st[j] + model.r[j]
model.total_chargers_equality = Constraint(model.F, rule=total_chargers)

# Demand per zone
def inner_value(model, zeta):
	value = sum(model.H[j,zeta] * model.y[j] for j in model.F)
	return value
def demand(model, z):
	value = sum(model.A[z,zeta] * inner_value(model, zeta)  for zeta in model.Z)
	return value >= model.gamma * model.dem[z]
model.demand_bound = Constraint(model.Z, rule=demand)

# On-street CPs
def on_street(model, z):
	value = sum(model.a[j] * model.H[j,z] * model.y[j] for j in model.F)
	return value <= model.Nz[z]
model.on_street_limit = Constraint(model.Z, rule=on_street)

# y_j <= cap_j 
def capacity(model, j):
	return model.y[j] <= model.cap[j]
model.capacity_limit = Constraint(model.F, rule=capacity)




def printOptimal():
	instance = model.create_instance("amplData.dat")
	# instance.display()
	opt = pyomo.opt.SolverFactory("glpk")
	results=opt.solve(instance)
	# instance.solutions.store_to(results)
	# print(results)
	if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
		print("\nfeasible")
	else:
		print("\ninfeasible")

	print("\nObjective is: ", value(instance.cost))

	print("\nConnectivity (x[i][j]): ")
	for i in range(len(instance.V)):
		for j in range(len(instance.F)):
			print(value(instance.x[i+1,j+1]))
		print("\n\n")
	print("\nFacilities (omega): ")
	for j in range(len(instance.F)):
		print(value(instance.omega[j+1]))
	print("\nStandard chargers: ")
	for j in range(len(instance.F)):
		print(value(instance.st[j+1]))
	print("\nRapid chargers: ")
	for j in range(len(instance.F)):
		print(value(instance.r[j+1]))
	print("\nAll chargers: ")
	for j in range(len(instance.F)):
		print(value(instance.y[j+1]))
