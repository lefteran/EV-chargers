# import read_data as rdt
# import distMatrix as dmtx
import parameters as pam
import _pickle as pickle

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
			self.x[vehicleKey] = xFacilitiesDict
		for facilityKey, _ in parameters.facilitiesDict.items():
			self.omega[facilityKey] = 1
			self.st[facilityKey] = 0
			self.r[facilityKey] = 0
			self.y[facilityKey] = 0

	# def set_values(self, parameters, x, omega, st, r, y):
	# 	self.x = x
	# 	self.omega = omega
	# 	self.st = st
	# 	self.r = r
	# 	self.y = y
	# 	if len(x) != parameters.Nov or len(x[0]) != parameters.Nof \
	# 	or len(omega) != parameters.Nof or len(st) != parameters.Nof or len(r) != parameters.Nof\
	# 	or len(y) != parameters.Nof:
	# 		print("*** Incorrect size of arrays in solution ***")
	# 	for i in range(parameters.Nof):
	# 		if self.st[i] + self.r[i] != self.y[i]:
	# 			print("*** The sum of standard and rapid chargers does not match the total chargers ***")


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
				# print("constraint 1 and vehicle key is ", vehicleKey)
				return False

		# ############### VEHICLE - FACILITY CONSTRAINTS ###############
		for vehicleKey, _ in parameters.vehiclesDict.items():
			for facilityKey, _ in parameters.facilitiesDict.items():
				# omega_j >= x_{ij}
				if self.omega[facilityKey] < self.x[vehicleKey][facilityKey]:
					# print("constraint 2 and facility key is ", facilityKey)
					return False
				# Binary variables
				if self.x[vehicleKey][facilityKey] < 0 or (self.x[vehicleKey][facilityKey] > 0\
				and self.x[vehicleKey][facilityKey] < 1) or self.x[vehicleKey][facilityKey] > 1\
				or self.omega[facilityKey] < 0 or (self.omega[facilityKey] > 0\
				and self.omega[facilityKey] < 1) or self.omega[facilityKey] > 1:
					# print("constraint 3 and facility key is ", facilityKey)
					return False			

		# ############### FACILITY ONLY CONSTRAINTS ###############
		for facilityKey, _ in parameters.facilitiesDict.items():
			# y_j >= omega_j
			if self.y[facilityKey] < self.omega[facilityKey]:
				# print("constraint 4 and facility key is ", facilityKey)
				return False
			# y_j (1 - omega_j) >= 0
			if self.y[facilityKey] * (1 - self.omega[facilityKey]) < 0:
				# print("constraint 5 and facility key is ", facilityKey)
				return False
			# y_j = y_j^{st} + y_j^r
			if self.y[facilityKey] != self.st[facilityKey] + self.r[facilityKey]:
				# print("constraint 6 and facility key is ", facilityKey)
				return False
			# capacity constraint
			if self.y[facilityKey] > parameters.facilitiesDict[facilityKey].capacity:
				# print("constraint 7 and facility key is ", facilityKey)
				return False
			# Integer variables
			if (not float(self.y[facilityKey]).is_integer()) or  (not float(self.st[facilityKey]).is_integer())\
			or (not float(self.r[facilityKey]).is_integer()):
				# print("constraint 8 and facility key is ", facilityKey)
				return False

		# ############### GLOBAL CONSTRAINTS ###############
		# sum of y_j^r >= R
		if sum(self.r.values()) < parameters.R:
			# print("constraint 9")
			return False

		# ############### ZONE CONSTRAINTS ###############
		for zoneKey, zoneObject in parameters.zonesDict.items():
			# Demand constraint
			zoneDeamand = self.currentDemand(parameters, zoneKey)
			if zoneDeamand < parameters.gamma * zoneObject.demand:
				# print("constraint 10 and zonekey is ", zoneKey)
				return False
			# On-street constraint
			zoneOnstreetCPs = self.zoneOnstreetCPs(parameters.zonesDict[zoneKey].facilities, parameters.facilitiesDict)
			if zoneOnstreetCPs > parameters.zonesDict[zoneKey].onStreetBound:
				# print("constraint 11 and zonekey is ", zoneKey)
				return False
		return True

	def isFeasibleWithReducedCPs(self, parameters, facilityId):
		# y_j >= omega_j
		if self.y[facilityId] < self.omega[facilityId]:
			return False
		# y_j (1 - omega_j) >= 0
		if self.y[facilityId] * (1 - self.omega[facilityId]) < 0:
			return False
		# sum of y_j^r >= R
		if sum(self.r.values()) < parameters.R:
			return False

		# ############### ZONE CONSTRAINTS ###############
		zoneId = parameters.facilitiesDict[facilityId].zoneId
		adjacentZoneIds = parameters.zonesDict[zoneId].adjacent
		for zoneKey in adjacentZoneIds:
			zoneObject = parameters.zonesDict[zoneKey]
			# DEMAND CONSTRAINT
			zoneDemand = self.currentDemand(parameters, zoneKey)
			if zoneDemand < parameters.gamma * zoneObject.demand:
				return False
			# OM-STREET CONSTRAINT
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

	def closeRedundantFacilities(self, parameters):
		for facilityKey, _ in parameters.facilitiesDict.items():
			if self. is_open(facilityKey) and self.y[facilityKey] == 0:
				self.connectVehiclesToNewFacility(parameters, facilityKey)
				self.close_facility(facilityKey)

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

	def isConnected(self, vehicleId, facilityId):
		return self.x[vehicleId][facilityId]

	def connect(self, vehicleId, facilityId):
		self.x[vehicleId][facilityId] = 1

	def disconnect(self, vehicleId, facilityId):
		self.x[vehicleId][facilityId] = 0

	def connectVehiclesToNewFacility(self, parameters, facilityId):
		vehicleIdsList = []
		for vehicleKey, _ in parameters.vehiclesDict.items():
			if self.isConnected(vehicleKey, facilityId):
				vehicleIdsList.append(vehicleKey)
				self.disconnect(vehicleKey, facilityId)
		for vehicleId in vehicleIdsList:
			self.connectVehicleToClosestFacility(parameters, vehicleId, facilityId)

	def getOpenFacilityToConnect(self, parameters, facilityToRemove):
		for facilityKey, _ in parameters.facilitiesDict.items():
			if self.is_open(facilityKey) and (facilityKey != facilityToRemove):
				return facilityKey

	def connectVehicleToClosestFacility(self, parameters, vehicleId, facilityToRemove):
		initialFacilityKey = self.getOpenFacilityToConnect(parameters, facilityToRemove)
		closest = parameters.timesDict[vehicleId][initialFacilityKey]
		closestFacility = initialFacilityKey
		for facilityKey, _ in parameters.facilitiesDict.items():
			if facilityKey != facilityToRemove:
				if (parameters.timesDict[vehicleId][facilityKey] < closest) and self.is_open(facilityKey):
					closest = parameters.timesDict[vehicleId][facilityKey]
					closestFacility = facilityKey
		self.connect(vehicleId, closestFacility)

	def getCost(self, parameters):
		cost = 0
		for i in range(parameters.Nov):
			for j in range(parameters.Nof):
				cost += parameters.distMatrix[i][j] * self.x[i][j]
		return cost

	def getCostLagrangian(self, parameters, lambdaVal):
		lagrangianCost = 0
		for i in range(parameters.Nov):
			for j in range(parameters.Nof):
				lagrangianCost += parameters.distMatrix[i][j] * self.x[i][j]
		lagrangianCost -= lambdaVal * parameters.B
		for j in range(parameters.Nof):
			lagrangianCost += lambdaVal *( parameters.c[j] * self.omega[j] + parameters.cst * self.st[j] + parameters.cr * self.r[j])
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

	# REDUCE THE NUMBER OF CHARGING POINTS PER FACILITY MAINTAINING FEASIBILITY
	def reduceCPs(self, parameters):
		count = 0
		total = len(parameters.facilitiesDict)
		for facilityKey, _ in parameters.facilitiesDict.items():
			count += 1
			print("facility %d of %d" %(count, total))
			for i in range(self.r[facilityKey]):
				self.removeRapidCP(facilityKey)
				if not self.isFeasibleWithReducedCPs(parameters, facilityKey):
					self.increaseRapidCP(facilityKey)
					break
			for i in range(self.st[facilityKey]):
				self.removeStandardCP(facilityKey)
				if not self.isFeasibleWithReducedCPs(parameters, facilityKey):
					self.increaseStandardCP(facilityKey)
					break

	def isFacilityFull(self, facility):
		return self.y[facility.id] == facility.capacity
		
	def hasFacilityStandardCPs(self, facId):
		return self.st[facId] != 0

	def hasFacilityRapidCPs(self, facId):
		return self.r[facId] != 0

	def getNextNotFullFacility(self, sortedByCapacity, index):
		for i in range(index, len(sortedByCapacity)):
			facility = sortedByCapacity[i]
			if not self.isFacilityFull(facility):
				return sortedByCapacity[i]
		return None

	def reassignVehiclesToFacilities(self, parameters, facilityId):
		vehicleIdsList = []
		for vehicleKey, _ in parameters.vehiclesDict.items():
			if self.isConnected(vehicleKey, facilityId):
				vehicleIdsList.append(vehicleKey)
				self.disconnect(vehicleKey, facilityId)
		for vehicleId in vehicleIdsList:
			self.connectVehicleToClosestFacility(parameters, vehicleId, facilityId)


	# REDISTRIBUTE THE CHARGING POINTS TO OTHER FACILITIES TO HAVE AS LESS FACILITIES OPEN AS POSSIBLE
	def redistributeCPs(self, parameters, zoneFacilities):
		if len(zoneFacilities) == 1:
			return
		sortedByCapacity = sorted(zoneFacilities, key=lambda x: x.capacity, reverse=True)
		index = 0
		facilityToFill = self.getNextNotFullFacility(sortedByCapacity, index)
		if facilityToFill == None:
			return
		for facilityToEmpty in sortedByCapacity[::-1]:
			standardCPsToMove = self.st[facilityToEmpty.id]
			rapidCPsToMove = self.r[facilityToEmpty.id]
			for i in range(standardCPsToMove):
				if facilityToEmpty.id == facilityToFill.id:
					break
				self.increaseStandardCP(facilityToFill.id)
				self.removeStandardCP(facilityToEmpty.id)
				if (not self.hasFacilityStandardCPs(facilityToEmpty.id)) and (not self.hasFacilityRapidCPs(facilityToEmpty.id)):
					self.reassignVehiclesToFacilities(parameters, facilityToEmpty.id)
					self.close_facility(facilityToEmpty.id)
				if self.isFacilityFull(facilityToFill):
					facilityToFill = self.getNextNotFullFacility(sortedByCapacity, index)
				if facilityToFill == None:
					return
			for i in range(rapidCPsToMove):
				if facilityToEmpty.id == facilityToFill.id:
					break
				self.increaseRapidCP(facilityToFill.id)
				self.removeRapidCP(facilityToEmpty.id)
				if (not self.hasFacilityStandardCPs(facilityToEmpty.id)) and (not self.hasFacilityRapidCPs(facilityToEmpty.id)):
					self.reassignVehiclesToFacilities(parameters, facilityToEmpty.id)
					self.close_facility(facilityToEmpty.id)
				if self.isFacilityFull(facilityToFill):
					facilityToFill = self.getNextNotFullFacility(sortedByCapacity, index)
				if facilityToFill == None:
					return
		

	# EXPORT OBJECT TO FILE
	def exportSolutionObject(self):
		with open('Chicago/solutionObject.pkl', 'wb') as solOutput:
			pickle.dump(self, solOutput, -1)


