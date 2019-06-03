class dataClass:
	def __init__(self):
		self.facilitiesDict = {}
		self.zonesDict = {}
		self.vehiclesDict = {}
		self.belongingDict = {}
		self.adjacencyDict = {}
		self.timesDict = {}
		self.standardCost = 25
		self.rapidCost = 38
		self.budget = 400000000
		self.facilitiesNo = 0
		self.zonesNo = 0
		self.vehiclesNo = 0
		self.gamma = 0.5
		self.R = 10
		self.lambdaMax = 10
		self.epsilon = 2
		self.swaps = 2