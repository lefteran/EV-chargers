import generalFuncs as gn

class Solution:

	def __init__(self, parameters):
	  	self.x = [ [0] * parameters.Nof ] * parameters.Nov
	  	self.omega = [0] * parameters.Nof
	  	self.st = [0] * parameters.Nof
	  	self.r = [0] * parameters.Nof
	  	self.y = [0] * parameters.Nof

	def set_values(self, parameters, x, omega, st, r, y):
		self.x = x
		self.omega = omega
		self.st = st
		self.r = r
		self.y = y
		if len(x) != parameters.Nov or len(x[0]) != parameters.Nof \
		or len(omega) != parameters.Nof or len(st) != parameters.Nof or len(r) != parameters.Nof\
		or len(y) != parameters.Nof:
			print("*** Incorrect size of arrays in solution ***")
		for i in range(parameters.Nof):
			if self.st[i] + self.r[i] != self.y[i]:
				print("*** The sum of standard and rapid chargers does not match the total chargers ***")


	def isFeasible(self, parameters):
		# Budget constraint
		land_cost = sum(x * y for x, y in zip(parameters.c, self.omega))
		cp_cost = parameters.cst * sum(self.st) + parameters.cr * sum(self.r)
		print("Land and cp cost is %f" %(land_cost + cp_cost))
		if land_cost + cp_cost > parameters.B:
			return False

		# sum of x_{ij}
		for i in range(parameters.Nov):
			if sum(self.x[i]) < 1:
				return False

		# omega_j >= x_{ij}
		for i in range(parameters.Nov):
			for j in range(parameters.Nof):
				if self.omega[j] < self.x[i][j]:
					return False

		# y_j >= omega_j
		for j in range(parameters.Nof):
			if self.y[j] < self.omega[j]:
				return False

		# sum of y_j^r >= R
		if sum(self.r) < parameters.R:
			return False

		# y_j = y_j^{st} + y_j^r
		for j in range(parameters.Nof):
			if self.y[j] != self.st[j] + self.r[j]:
				return False

		# Demand constraint
		for z in range(parameters.Noz):
			total_value = gn.currentDemand(parameters, self, z)
			if total_value < parameters.gamma * parameters.demand[z]:
				return False

		# On-street constraint
		for z in range(parameters.Noz):
			value = gn.currentOnstreetCPs(parameters, self, z)
			if value > parameters.Nz[z]:
				return False

		# capacity constraint
		for j in range(parameters.Nof):
			if self.y[j] > parameters.cap[j]:
				return False

		# Binary variables
		for i in range(parameters.Nov):
			for j in range(parameters.Nof):
				if self.x[i][j] < 0 or (self.x[i][j] > 0 and self.x[i][j] < 1) or self.x[i][j] > 1\
				or self.omega[j] < 0 or (self.omega[j] > 0 and self.omega[j] < 1) or self.omega[j] > 1:
					return False			

		# Integer variables
		for j in range(parameters.Nof):
			if (not float(self.y[j]).is_integer()) or  (not float(self.st[j]).is_integer()) or (not float(self.r[j]).is_integer()):
				return False

		return True


	def open_facility(self, facility):
		self.omega[facility] = 1

	def close_facility(self, facility):
		self.omega[facility] = 0
		self.st[facility] = 0
		self.r[facility] = 0
		self.y[facility] = 0

	def is_open(self, facility):
		return self.omega[facility]

	def connect(self, vehicle, facility):
		self.x[vehicle][facility] = 1

	def disconnect(self, vehicle, facility):
		self.x[vehicle][facility] = 0

	def cost(self, parameters):
		vehicleCost = 0	
		scenCost = 0
		facCost = 0

		scenCosts = []
		for scenario in range(parameters.Nos):
			vehCosts=[]
			for vehicle in range(parameters.Nov):
				facCosts = []
				for facility in range(parameters.Nof):
					facCost = parameters.beta[vehicle][facility]\
					* parameters.dist[scenario][vehicle][facility]\
					* self.x[vehicle][facility]
					facCosts.append(facCost)
					# print("Facility %d cost is %f" %(facility, facCost))
				vehicleCost = sum(facCosts)
				# print("Vehicle %d cost is %f\n" %(vehicle, vehicleCost))
				vehCosts.append(vehicleCost)
			scenCost = sum(vehCosts)
			# print("Scenario %d cost is %f\n\n" %(scenario, scenCost))
			scenCosts.append(scenCost)		
		return sum(scenCosts)