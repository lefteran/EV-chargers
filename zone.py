class Zone:
	def __init__(self, idNum, adjacent, demand, facilities, onStreetBound):
		self.id = idNum
		self.demand = demand
		self.adjacent = adjacent
		self.facilities = facilities
		self.onStreetBound = onStreetBound
		self.polygon = []