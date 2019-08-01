from sys import stderr, exit

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

		self.gamma = 0.5
		self.R = 10
		self.lambdaMax = 10
		self.epsilon = 2
		self.swaps = 2

		self.candidateLocations = []
		self.numberOfVehicles = 30
		self.radius = 0.1

		self.vehiclesClosestTuples = {}
		self.removedFacilityIds = []
		self.k = 50  # NUMBER OF FACILITIES TO BE OPENED
		self.C = 1000
		self.r = 100
		self.p = 2

		self.algorithm = 1
		self.algorithmDict = {1: "Forward Greedy",
						 2: "Backward Greedy",
						 3: "Random Local Search"}

class Flags:
	def __init__(self):
		self.doPreprocessing = False

		self.importTimes = False
		self.useGraphTool = True
		self.parallelComputationOfTimes = True
		self.importVehiclesDict = False

		self.saveNetwork = False

class FilePaths:
	def __init__(self):
		self.clustersFile = 'scenariosData/clustering_' + str(parameters.radius) + '.json'
		self.fwdGreedyFile = "data/solutions/fwdGreedy/fwdGreedy_" + str(parameters.k) + '_' + str(parameters.radius) + ".json"
		self.backGreedyFile = "data/solutions/backGreedy/backGreedy_" + str(parameters.k) + '_' + str(parameters.radius) + ".json"
		self.randomLocalSearchFile = "data/solutions/randomLocalSearch/rndLocalSearch_" + str(parameters.k) + '_' + str(parameters.radius) + ".json"
		self.clusterFilename = 'data/scenariosData/' + str(parameters.radius) + '/clustering_' + str(parameters.radius) + '.json'
		self.vehiclesDictFile = 'data/scenariosData/' + str(parameters.radius) + '/vehiclesDict_' + str(parameters.numberOfVehicles) + '.json'
		self.timesDictFile = 'data/scenariosData/' + str(parameters.radius) + '/timesDict_' + str(parameters.numberOfVehicles) + '_' + str(parameters.radius) + '.csv'


def init():
	global parameters
	parameters = Parameters()
	global flags
	flags = Flags()
	global filePaths
	filePaths = FilePaths()
	global places
	places = {'london': 'Greater London, England, United Kingdom',
			'piedmont': 'Piedmont, California',
			'chicago': 'Chicago, Cook County, Illinois, USA'}