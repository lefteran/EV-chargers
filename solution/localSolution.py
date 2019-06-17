class localSolution:
	def __init__(self, parameters, S, zoneId):
		self.x = {}
		self.omega = {}
		self.st = {}
		self.r = {}
		self.y = {}
		for facility in parameters.zonesDict[zoneId].facilities:
			self.omega[facility.id] = S.omega[facility.id]
			self.st[facility.id] = S.st[facility.id]
			self.r[facility.id] = S.r[facility.id]
			self.y[facility.id] = S.y[facility.id]
		for vehicleKey, _ in parameters.vehiclesDict.items():
			xFacilitiesDict = {}
			for facility in parameters.zonesDict[zoneId].facilities:
				xFacilitiesDict[facility.id] = 0
			self.x[vehicleKey] = xFacilitiesDict