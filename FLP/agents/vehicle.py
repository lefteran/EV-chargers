# FILES
import settings

class Vehicle:
	def __init__(self, idNum, startNode, endNode, rn):
		self.id = idNum
		self.startNode = startNode
		self.endNode = endNode
		self.pointInEdge = rn


	def getClosestFacilities_TimesTuples(self):
		closestFacilities = []
		# for facilityKey, _ in settings.facilitiesDict.items():
		for facilityId in settings.candidateLocations:
			timeToFacility = settings.timesDict[str(self.id)][facilityId]
			closestFacilities.append((facilityId, timeToFacility))
		closestFacilities.sort(key=lambda tup: tup[1])
		return closestFacilities


	def getNearestFacility(self, facilities):
		timeToFacility = float("inf")
		closestFacility = None
		for facilityId in facilities:
			if settings.timesDict[self.id][facilityId] < timeToFacility:
				timeToFacility = settings.timesDict[self.id][facilityId]
				closestFacility = facilityId
		return closestFacility

	def getTimeToNearestFacility(self, facilities):
		timeToFacility = float("inf")
		for facilityId in facilities:
			if facilityId == None:
				a=2
			if settings.timesDict[str(self.id)][facilityId] < timeToFacility:
				timeToFacility = settings.timesDict[str(self.id)][facilityId]
		return timeToFacility

	def updateNearestFacilityTime(self, facilities):
		timeToFacility = float("inf")
		closestFacility = None
		for facilityId in facilities:
			if settings.timesDict[self.id][facilityId] < timeToFacility:
				timeToFacility = settings.timesDict[self.id][facilityId]
				closestFacility = facilityId
		settings.closestFacilitiesDict[self.id] = closestFacility
		return timeToFacility