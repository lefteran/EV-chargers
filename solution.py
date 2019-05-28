# import read_data as rdt
# import distMatrix as dmtx
import parameters as pam

class Solution:
	def __init__(self, parameters):
		self.x = {}
		self.omega = {}
		self.st = {}
		self.r = {}
		self.y = {}
		for vehicleKey, _ in parameters.vehiclesDict.items():
			xFacilitiesDict = {}
			for facilityKey, _ in parameters.facilitiesDict.items():
				xFacilitiesDict[facilityKey] = 0
				self.omega[facilityKey] = 1
				self.st[facilityKey] = 0
				self.r[facilityKey] = 0
				self.y[facilityKey] = 0
			self.x[vehicleKey] = xFacilitiesDict

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


	def IsFeasibleWithBudget(self, parameters):
		# Budget constraint
		land_cost = 0
		for facilityKey, facilityObject in parameters.facilitiesDict.items():
			land_cost += facilityObject.cost * self.omega[facilityKey]
		cp_cost = parameters.standardCost * sum(self.st.values()) + parameters.rapidCost * sum(self.r.values())
		if land_cost + cp_cost > parameters.budget:
			return False
		return self.isFeasibleWithoutBudget(parameters)

	def isFeasibleWithoutBudget(self, parameters):
		# ############### VEHICLE ONLY CONSTRAINTS ###############
		# sum of x_{ij}
		for vehicleKey, _ in parameters.vehiclesDict.items():
			if sum(self.x[vehicleKey].values()) < 1:
				return False

		# ############### VEHICLE - FACILITY CONSTRAINTS ###############
		for vehicleKey, _ in parameters.vehiclesDict.items():
			for facilityKey, _ in parameters.facilitiesDict.items():
				# omega_j >= x_{ij}
				if self.omega[facilityKey] < self.x[vehicleKey][facilityKey]:
					return False
				# Binary variables
				if self.x[vehicleKey][facilityKey] < 0 or (self.x[vehicleKey][facilityKey] > 0\
				and self.x[vehicleKey][facilityKey] < 1) or self.x[vehicleKey][facilityKey] > 1\
				or self.omega[facilityKey] < 0 or (self.omega[facilityKey] > 0\
				and self.omega[facilityKey] < 1) or self.omega[facilityKey] > 1:
					return False			

		# ############### FACILITY ONLY CONSTRAINTS ###############
		for facilityKey, _ in parameters.facilitiesDict.items():
			# y_j >= omega_j
			if self.y[facilityKey] < self.omega[facilityKey]:
				return False
			# y_j (1 - omega_j) >= 0
			if self.y[facilityKey] * (1 - self.omega[facilityKey]) < 0:
				return False
			# y_j = y_j^{st} + y_j^r
			if self.y[facilityKey] != self.st[facilityKey] + self.r[facilityKey]:
				return False
			# capacity constraint
			if self.y[facilityKey] > parameters.facilitiesDict[facilityKey].capacity:
				return False
			# Integer variables
			if (not float(self.y[facilityKey]).is_integer()) or  (not float(self.st[facilityKey]).is_integer())\
			or (not float(self.r[facilityKey]).is_integer()):
				return False

		# ############### GLOBAL CONSTRAINTS ###############
		# sum of y_j^r >= R
		if sum(self.r.values()) < parameters.R:
			return False

		# ############### ZONE CONSTRAINTS ###############
		for zoneKey, zoneObject in parameters.zonesDict.items():
			# Demand constraint
			zoneDeamand = self.currentDemand(parameters, zoneKey)
			if zoneDeamand < parameters.gamma * zoneObject.demand:
				return False
			# On-street constraint
			zoneOnstreetCPs = self.zoneOnstreetCPs(parameters.zonesDict[zoneKey].facilities, parameters.facilitiesDict)
			if zoneOnstreetCPs > parameters.zonesDict[zoneKey].onStreetBound:
				return False
		return True


	def currentDemand(self, parameters, zoneId):
		value = 0
		for zetaId in parameters.zonesDict[zoneId].adjacent:
			for facilityId in parameters.zonesDict[zetaId].facilities:
				value += self.y[facilityId]
		return value

	def zoneOnstreetCPs(self, zoneFacilityIds, facilitiesDict):
		value = 0
		for facilityId in zoneFacilityIds:
			value += facilitiesDict[facilityId].alpha * self.y[facilityId]
		return value

	def open_facility(self, facilityId):
		self.omega[facilityId] = 1

	def close_facility(self, facilityId):
		self.omega[facilityId] = 0
		self.st[facilityId] = 0
		self.r[facilityId] = 0
		self.y[facilityId] = 0

	def is_open(self, facilityId):
		return self.omega[facilityId]

	def canRemoveRapidCP(self, facility):
		return True if self.r[facility] > 0 else False

	def canRemoveStandardCP(self, facility):
		return True if self.st[facility] > 0 else False

	def removeRapidCP(self, facilityId):
		self.r[facilityId] -= 1
		self.y[facilityId] -= 1

	def removeStandardCP(self, facilityId):
		self.st[facilityId] -= 1
		self.y[facilityId] -= 1

	def increaseRapidCP(self, facilityId):
		self.r[facilityId] += 1
		self.y[facilityId] += 1

	def increaseStandardCP(self, facilityId):
		self.st[facilityId] += 1
		self.y[facilityId] += 1

	def connect(self, vehicleId, facilityId):
		self.x[vehicleId][facilityId] = 1

	def disconnect(self, vehicle, facility):
		self.x[vehicle][facility] = 0

	def getCost(self, parameters):
		cost = 0
		for i in range(parameters.Nov):
			for j in range(parameters.Nof):
				cost += parameters.distMatrix[i][j] * self.x[i][j]
		return cost

	def getCostLagrangian(self, parameters, lambdaVal):
		lagrangianCost = 0
		# lambdaFactorsCost = 0
		for i in range(parameters.Nov):
			for j in range(parameters.Nof):
				lagrangianCost += parameters.distMatrix[i][j] * self.x[i][j]
		# print("Initially cost is %.2f" %lagrangianCost)
		lagrangianCost -= lambdaVal * parameters.B
		# print("Budget factor  is %.2f" %(lambdaVal * parameters.B))
		for j in range(parameters.Nof):
			# lambdaFactorsCost += lambdaVal *( parameters.c[j] * self.omega[j] + parameters.cst * self.st[j] + parameters.cr * self.r[j])
			lagrangianCost += lambdaVal *( parameters.c[j] * self.omega[j] + parameters.cst * self.st[j] + parameters.cr * self.r[j])
		# print("lambda factors cost is %.2f" %lambdaFactorsCost)
		return lagrangianCost

	def printSol(self, parameters, lambdaVal):
		print("x is ", self.x)
		print("st is ", self.st)
		print("r is ", self.r)
		print("y is ", self.y)
		print("omega is ", self.omega)
		print("Cost of objective is %.2f" %self.getCost(parameters))
		print("Cost of lagrangian objective is %.2f" %self.getCostLagrangian(parameters, lambdaVal))
		print("Solution feasible (without budget): %r" %self.isFeasibleWithoutBudget(parameters))
		print("Solution feasible (with budget): %r" %self.IsFeasibleWithBudget(parameters))


# parameters = pam.Parameters()
# testSol = Solution(parameters)
# cost = testSol.getCost(parameters)
# print(cost)