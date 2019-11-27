import _pickle as pickle

class globalPartOfSolution:
	def __init__(self, parameters, S):
		self.x = {}
		for vehicleKey, _ in parameters.vehiclesDict.items():
			self.x[vehicleKey] = S.x[vehicleKey]
			# xFacilitiesDict = {}
			# for facilityKey, _ in parameters.facilitiesDict.items():
			# 	xFacilitiesDict[facilityKey] = S.x[vehicleKey][facilityKey]
			# self.x[vehicleKey] = xFacilitiesDict


	# def setNewValues(self, parameters, tempGlobalPart):
	# 	for vehicleKey, _ in parameters.vehiclesDict.items():
	# 		for facilityKey, _ in parameters.facilitiesDict.items():
	# 			self.x[vehicleKey][facilityKey].value = tempGlobalPart.x[vehicleKey][facilityKey]


class tempGlobalPartMapping(dict):
	def setDict(self, globalPart):
		self.__dict__ = pickle.loads(pickle.dumps(dict(globalPart), -1))

	def setValue(self, vehicleId, facilityId, value):
		self.__dict__[vehicleId][facilityId] = value

	def getVehicleDict(self, vehicleId):
		return self.__dict__[vehicleId]

	def isConnectedPrl(self, vehicleId, facilityId):
		return self.__dict__[vehicleId][facilityId]

	def connectPrl(self, vehicleId, facilityId):
		self.__dict__[vehicleId][facilityId] = 1

	def disconnectPrl(self, vehicleId, facilityId):
		self.__dict__[vehicleId][facilityId] = 0

	def subtractDisconnectedPairTimesPrl(self, parameters, disconnectedPairs):
		disconnectionSubtractedCost = 0
		for pair in disconnectedPairs:
			disconnectionSubtractedCost += parameters.timesDict[pair[0]][pair[1]]
		return disconnectionSubtractedCost

	def addConnectedPairTimesPrl(self, parameters, connectedPairs):
		connectionAddedCost = 0
		for pair in connectedPairs:
			connectionAddedCost += parameters.timesDict[pair[0]][pair[1]]
		return connectionAddedCost

	def getAnyOpenFacilityToConnectPrl(self, localPartsDict, zoneId, facilityToRemove):
		for zoneKey, _ in localPartsDict.items():
			if zoneKey != zoneId:
				for facilityKey, _ in localPartsDict[zoneKey].omega.items():
					if localPartsDict[zoneKey].is_openPrl(facilityKey) and (facilityKey != facilityToRemove):
						return facilityKey
		return -1

	def connectVehicleToClosestFacilityPrl(self, newLocalPart, localPartsDict, zoneId, parameters, vehicleId, facilityToRemove):
		initialFacilityKey = self.getAnyOpenFacilityToConnectPrl(localPartsDict, zoneId, facilityToRemove)
		closest = parameters.timesDict[vehicleId][initialFacilityKey]
		closestFacility = initialFacilityKey
		for zoneKey, _ in localPartsDict.items():
			if zoneKey != zoneId:
				for facilityKey, _ in localPartsDict[zoneKey].omega.items():
					if (parameters.timesDict[vehicleId][facilityKey] < closest) and localPartsDict[zoneKey].is_openPrl(facilityKey) and (facilityKey != facilityToRemove):
						closest = parameters.timesDict[vehicleId][facilityKey]
						closestFacility = facilityKey
		# CHECK THE LOCAL PART OF THE NEW SOLUTION SEPARATELY
		for facilityKey, _ in newLocalPart.omega.items():
			if (parameters.timesDict[vehicleId][facilityKey] < closest) and newLocalPart.is_openPrl(facilityKey) and (facilityKey != facilityToRemove):
				closest = parameters.timesDict[vehicleId][facilityKey]
				closestFacility = facilityKey
		self.connectPrl(vehicleId, closestFacility)
		return closestFacility

	def connectVehiclesToNewFacilityPrl(self, newLocalPart, localPartsDict, zoneId, parameters, facilityId):
		vehicleIdsList = []
		disconnectedPairs = []
		connectedPairs = []
		for vehicleKey, _ in parameters.vehiclesDict.items():
			if self.isConnectedPrl(vehicleKey, facilityId):
				vehicleIdsList.append(vehicleKey)
				self.disconnectPrl(vehicleKey, facilityId)
				disconnectedPairs.append((vehicleKey, facilityId))
		disconnectionSubtractedCost = self.subtractDisconnectedPairTimesPrl(parameters, disconnectedPairs)
		for vehicleId in vehicleIdsList:
			closestFacility = self.connectVehicleToClosestFacilityPrl(newLocalPart, localPartsDict, zoneId, parameters, vehicleId, facilityId)
			connectedPairs.append((vehicleId, closestFacility))
		connectionAddedCost = self.addConnectedPairTimesPrl(parameters, connectedPairs)
		return connectionAddedCost - disconnectionSubtractedCost


class localPartOfSolution:
	def __init__(self, parameters, S, zoneId):
		self.omega = {}
		self.st = {}
		self.r = {}
		self.y = {}
		for facilityId in parameters.zonesDict[zoneId].facilities:
			self.omega[facilityId] = S.omega[facilityId]
			self.st[facilityId] = S.st[facilityId]
			self.r[facilityId] = S.r[facilityId]
			self.y[facilityId] = S.y[facilityId]

	def is_openPrl(self, facilityId):
		return self.omega[facilityId]

	def openFacilityPrl(self, facilityId):
		self.omega[facilityId] = 1

	def closeFacilityPrl(self, facilityId):
		self.omega[facilityId] = 0
		self.st[facilityId] = 0
		self.r[facilityId] = 0
		self.y[facilityId] = 0

	def setNewValues(self, parameters, newLocalPart, zoneId):
		for facilityId in parameters.zonesDict[zoneId].facilities:
			self.omega[facilityId] = newLocalPart.omega[facilityId]
			self.st[facilityId] = newLocalPart.st[facilityId]
			self.r[facilityId] = newLocalPart.r[facilityId]
			self.y[facilityId] = newLocalPart.y[facilityId]