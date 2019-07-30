import collections

class Cluster:
	def __init__(self, candidateLocations, time, radius):
		self.candidateLocations = candidateLocations
		self.time = time
		self.radius = radius


	def hasDuplicates(self):
		if len([item for item, count in collections.Counter(self.candidateLocations).items() if count > 1]) > 0:
			return True
		else:
			return False

