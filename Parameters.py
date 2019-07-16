import _pickle as pickle

class Parameters:
	def __init__(self):
		self.facilitiesDict = {}
		self.zonesDict = {}
		self.belongingDict = {}
		self.adjacencyDict = {}

		self.vehiclesDict = {}
		self.timesDict = {}

		self.standardCost = 25
		self.rapidCost = 38
		self.budget = 400000000
		# self.facilitiesNo = 0
		# self.zonesNo = 0
		# self.vehiclesNo = 0
		self.gamma = 0.5
		self.R = 10
		self.lambdaMax = 10
		self.epsilon = 2
		self.swaps = 2

		self.doPreprocessing = False
		self.importSolution = True
		self.importTimes = True
		self.useGraphTool = True
		self.parallelComputationOfTimes = True
		self.exportParametersFlag = True
		self.importParametersFlag = False
		self.importVehiclesDict = True
		self.parallelLocalSearch = True


	def exportParameters(self, filename):
		with open(filename, 'wb') as parametersOutput:
			pickle.dump(self, parametersOutput, -1)
