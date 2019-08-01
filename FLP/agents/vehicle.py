import settings

class Vehicle:
	def __init__(self, idNum, startNode, endNode, rn):
		self.id = idNum
		self.startNode = startNode
		self.endNode = endNode
		self.pointInEdge = rn


	def getClosestFacilities_TimesTuples(self):
		closestFacilities = []
		# for facilityKey, _ in settings.parameters.facilitiesDict.items():
		for facilityId in settings.parameters.candidateLocations:
			timeToFacility = settings.parameters.timesDict[self.id][facilityId]
			closestFacilities.append((facilityId, timeToFacility))
		closestFacilities.sort(key=lambda tup: tup[1])
		return closestFacilities


	def getNearestFacility(self, facilities):
		timeToFacility = float("inf")
		closestFacility = None
		for facilityId in facilities:
			if settings.parameters.timesDict[self.id][facilityId] < timeToFacility:
				timeToFacility = settings.parameters.timesDict[self.id][facilityId]
				closestFacility = facilityId
		return closestFacility

	def getNearestFacilityTime(self, facilities):
		timeToFacility = float("inf")
		for facilityId in facilities:
			if settings.parameters.timesDict[str(self.id)][facilityId] < timeToFacility:
				timeToFacility = settings.parameters.timesDict[str(self.id)][facilityId]
		return timeToFacility

	def updateNearestFacilityTime(self, facilities):
		timeToFacility = float("inf")
		closestFacility = None
		for facilityId in facilities:
			if settings.parameters.timesDict[self.id][facilityId] < timeToFacility:
				timeToFacility = settings.parameters.timesDict[self.id][facilityId]
				closestFacility = facilityId
		settings.parameters.closestFacilitiesDict[self.id] = closestFacility
		return timeToFacility