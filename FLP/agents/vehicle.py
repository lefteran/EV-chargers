# FILES
import settings

class Vehicle:
	def __init__(self, idNum, startNode, endNode, rn):
		self.id = idNum
		self.startNode = startNode
		self.endNode = endNode
		self.pointInEdge = rn
		self.timesToLocationsList = []
		self.tupleToListIndexDict = {}
		self.bestIndex = -1


	# ############## FOR LOCAL SEARCH #############################
	def createSortedListOfTuplesAndDictOfIndices(self):
		for facilityId in settings.candidateLocations:
			facilityTuple = (facilityId, settings.timesDict[str(self.id)][facilityId])
			self.timesToLocationsList.append(facilityTuple)
		self.timesToLocationsList.sort(key=lambda tup: tup[1])
		for index, sortedTuple in enumerate(self.timesToLocationsList):
			self.tupleToListIndexDict[sortedTuple[0]] = index

	def getTimeToNearestFacility1(self, facilities, newlyAddedFacilityId, removedFacilityId):
		if self.bestIndex == -1:
			bestTimeToFacility =  self.timesToLocationsList[self.tupleToListIndexDict[facilities[0]]][1]
			for facilityId in facilities:
				facilityListIndex = self.tupleToListIndexDict[facilityId]
				timeToFacility = self.timesToLocationsList[facilityListIndex][1]
				if timeToFacility < bestTimeToFacility:
					bestTimeToFacility = timeToFacility
					self.bestIndex = facilityListIndex
		else:
			indexOfNewFacility = self.tupleToListIndexDict[newlyAddedFacilityId]
			indexOfRemovedFacility = self.tupleToListIndexDict[removedFacilityId]
			if indexOfNewFacility < indexOfRemovedFacility:
				self.bestIndex = indexOfNewFacility
			else:
				if indexOfRemovedFacility == self.bestIndex:
					for facilityTuple in self.timesToLocationsList[indexOfRemovedFacility:]:
						if facilityTuple[0] in facilities:
							self.bestIndex = self.tupleToListIndexDict[facilityTuple[0]]
							break
		return self.timesToLocationsList[self.bestIndex][1]


	################################################################

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