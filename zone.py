class Zone:
	def __init__(self, idNum, adjacent, demand, facilities):
		self.id = idNum
		self.demand = demand
		self.adjacent = adjacent
		self.facilities = facilities