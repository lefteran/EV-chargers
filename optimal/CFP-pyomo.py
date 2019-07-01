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


# ### PARAMETERS ###
# Cost of each slow Charging Point
model.cs = Param(model.F, within=PositiveReals)
# Cost of each fast Charging Point
model.cf = Param(model.F, within=PositiveReals)
# Cost of each rapid Charging Point
model.cr = Param(model.F, within=PositiveReals)
# Capacity of each facility
model.cap = Param(model.F, within=PositiveIntegers)
# Indicator of type (on-off-street)
model.a = Param(model.F, within=Binary, mutable=True)
# Demand of each zone
model.dem = Param(model.Z, within=PositiveIntegers, mutable=True)
# Limit on the number of on-street spaces in zone z
model.Nz = Param(model.Z, within=PositiveIntegers)
# Binary (belonging) matrix denoting whether a facility belongs to a zone
model.B = Param(model.F, model.Z, within=Binary, mutable=True)
# Adjacency matrix denoting whether a zone is adjacent to another
model.A = Param(model.Z, model.Z, within=Binary, mutable=True)
# Minimum number of rapid chargers
model.R = Param(within=PositiveIntegers)
# Proportion of charging demand to be satisfied
model.gamma = Param(within=PositiveReals)



# ### VARIABLES ###
# Number of slow chargers per facility
model.s = Var(model.F, domain=NonNegativeIntegers, initialize=0)
# Number of fast chargers per facility
model.f = Var(model.F, domain=NonNegativeIntegers, initialize=0)
# Number of rapid chargers per facility
model.r = Var(model.F, domain=NonNegativeIntegers, initialize=0)
# # Number of all chargers per facility
model.y = Var(model.F, domain=NonNegativeIntegers, initialize=0)


# ### OBJECTIVE ###
# Minimize the cost of installing the CPs
def cost_rule(model):
	return sum(model.cs[i]*model.s[i] + model.cf[i]*model.f[i] + model.cr[i]*model.r[i] for i in model.F)
model.cost = Objective(rule=cost_rule)


# ### CONSTRAINTS ###

# Lower bound on the charging demand per zone
def inner_value(model, j):
	value = sum(model.B[i,j] * model.y[i] for i in model.F)
	return value
def demand(model, z):
	value = sum(model.A[z,j] * inner_value(model, j)  for j in model.Z)
	return value >= model.gamma * model.dem[z]
model.demand_bound = Constraint(model.Z, rule=demand)

# Total number of charging points $y_i$ at location $i$ is equal to the sum of 
# the slow $s_i$, fast $f_i$ and rapid $r_i$ charging points 
def total_chargers(model, i):
	return model.y[i] == model.s[i] + model.f[i] + model.r[i]
model.total_chargers_equality = Constraint(model.F, rule=total_chargers)

# Limit on the number of chargers per facility 
def rapid_chargers(model):
	return sum(model.r[i] for i in model.F) >= model.R
model.rapid_chargers_bound = Constraint(rule=rapid_chargers)

# Limit on the number of available spaces for on-street CPs
def on_street(model, z):
	value = sum(model.a[i] * model.B[i,z] * model.y[i] for i in model.F)
	return value <= model.Nz[z]
model.on_street_limit = Constraint(model.Z, rule=on_street)

# Limit on the number of chargers per facility 
def capacity(model, i):
	return model.y[i] <= model.cap[i]
model.capacity_limit = Constraint(model.F, rule=capacity)





instance = model.create_instance("CFP_data.dat")
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

print("\nSlow chargers: ")
for i in range(len(instance.F)):
	print(value(instance.s[i+1]))
print("\nFast chargers: ")
for i in range(len(instance.F)):
	print(value(instance.f[i+1]))
print("\nRapid chargers: ")
for i in range(len(instance.F)):
	print(value(instance.r[i+1]))
print("\nAll chargers: ")
for i in range(len(instance.F)):
	print(value(instance.y[i+1]))