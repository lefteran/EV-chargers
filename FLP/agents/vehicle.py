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
		self.previousBestIndex = -1
		self.potentialBestIndex = -1


	# ############## FOR LOCAL SEARCH #############################
	def createSortedListOfTuplesAndDictOfIndices(self):
		for facilityId in settings.candidateLocations:
			facilityTuple = (facilityId, settings.timesDict[str(self.id)][facilityId])
			self.timesToLocationsList.append(facilityTuple)
		self.timesToLocationsList.sort(key=lambda tup: tup[1])
		for index, sortedTuple in enumerate(self.timesToLocationsList):
			self.tupleToListIndexDict[sortedTuple[0]] = index


	def noBestIndex(self, facilities):
		for facilityTuple in self.timesToLocationsList:
			if facilityTuple[0] in facilities:
				bestTimeToFacility = facilityTuple[1]
				self.bestIndex = self.tupleToListIndexDict[facilityTuple[0]]
				self.potentialBestIndex = self.tupleToListIndexDict[facilityTuple[0]]
				return bestTimeToFacility


	def existingBestIndex(self, facilities, newlyAddedFacilityId, removedFacilityId, previousSolutionAccepted):
		if previousSolutionAccepted:
			self.bestIndex = self.potentialBestIndex

		# if self.timesToLocationsList[self.bestIndex][0] not in facilities:
		# 	a=2

		indexOfNewFacility = self.tupleToListIndexDict[newlyAddedFacilityId]
		indexOfRemovedFacility = self.tupleToListIndexDict[removedFacilityId]
		if indexOfNewFacility < self.bestIndex:
			# self.previousBestIndex = self.bestIndex
			self.potentialBestIndex = indexOfNewFacility
		else:
			if indexOfRemovedFacility == self.bestIndex:
				for facilityTuple in self.timesToLocationsList[indexOfRemovedFacility + 1:]:
					if facilityTuple[0] in facilities:
						# self.previousBestIndex = self.bestIndex
						self.potentialBestIndex = self.tupleToListIndexDict[facilityTuple[0]]			# AND potentialIndex not in removed facilities (for case of p = 2,3)
						break
			else:
				self.potentialBestIndex = self.bestIndex
		return self.timesToLocationsList[self.potentialBestIndex][1]


	def getTimeToNearestFacility1(self, facilities, newlyAddedFacilityId, removedFacilityId, previousSolutionAccepted):
		# if not previousSolutionAccepted:
		# 	self.bestIndex = self.previousBestIndex
		if self.bestIndex == -1:
			return self.noBestIndex(facilities)
		else:
			return self.existingBestIndex(facilities, newlyAddedFacilityId, removedFacilityId, previousSolutionAccepted)

	################################################################

	def getTimeToNearestFacility(self, facilities):
		timeToFacility = float("inf")
		for facilityId in facilities:
			if settings.timesDict[str(self.id)][facilityId] < timeToFacility:
				timeToFacility = settings.timesDict[str(self.id)][facilityId]
				bestFacility = facilityId						#TODO: THIS LINE TO BE DELETED LATER
		return timeToFacility

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


	def updateNearestFacilityTime(self, facilities):
		timeToFacility = float("inf")
		closestFacility = None
		for facilityId in facilities:
			if settings.timesDict[self.id][facilityId] < timeToFacility:
				timeToFacility = settings.timesDict[self.id][facilityId]
				closestFacility = facilityId
		settings.closestFacilitiesDict[self.id] = closestFacility
		return timeToFacility