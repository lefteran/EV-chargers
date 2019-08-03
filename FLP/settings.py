# ############################# Parameters #############################
facilitiesDict = {}
zonesDict = {}
belongingDict = {}
adjacencyDict = {}

vehiclesDict = {}
timesDict = {}

standardCost = 25
rapidCost = 38
budget = 400000000

gamma = 0.5
R = 10
lambdaMax = 10
epsilon = 2
swaps = 2

candidateLocations = []
numberOfVehicles = -1
radius = 0.1

vehiclesClosestTuples = {}
removedFacilityIds = []
k = 50				# NUMBER OF FACILITIES TO BE OPENED
C = 1000
r = 1000			# NUMBER OF ITERATIONS FOR THE RANDOM LOCAL SEARCH
p = 1				# NUMBER OF FACILITIES TO SWAP (IN RANDOM LOCAL SEARCH)

algorithm = 2
algorithmDict = {1: "Forward Greedy",
				 2: "Backward Greedy",
				 3: "Random Local Search"}

places = {'london': 'Greater London, England, United Kingdom',
		'piedmont': 'Piedmont, California',
		'chicago': 'Chicago, Cook County, Illinois, USA'}


# ############################# Flags #############################
doPreprocessing = False

importTimes = False
useGraphTool = True
parallelComputationOfTimes = True
importVehiclesDict = False

saveNetwork = False


# ############################# FilePaths #############################
scenarioDirectory = 'data/scenariosData/' + str(radius)
clustersFile = 'data/scenariosData/' + str(radius) + '/clustering_' + str(radius) + '.json'
clusterFilename = 'data/scenariosData/' + str(radius) + '/clustering_' + str(radius) + '.json'
vehiclesDictFile = 'data/scenariosData/' + str(radius) + '/vehiclesDict_' + str(numberOfVehicles) + '.json'
timesDictFile = 'data/scenariosData/' + str(radius) + '/timesDict_' + str(numberOfVehicles) + '_' + str(radius) + '.csv'


fwdGreedykDir = 'data/solutions/fwdGreedy/k_' + str(k)
fwdGreedyFile = 'data/solutions/fwdGreedy/k_' + str(k) + '/fwdGreedy_' + str(numberOfVehicles) + '_' + str(radius) + '.json'

backGreedykDir = 'data/solutions/backGreedy/k_' + str(k)
backGreedyFile = 'data/solutions/backGreedy/k_' + str(k) + '/backGreedy_' + str(numberOfVehicles) + '_' + str(radius) + '.json'

randomLocalSearchkDir = 'data/solutions/randomLocalSearch/k_' + str(k)
randomLocalSearchFile = 'data/solutions/randomLocalSearch/k_' + str(k) + '/rndLocalSearch_' + str(numberOfVehicles) + '_' + str(radius) + '.json'


def resetFilePaths():
	global scenarioDirectory
	scenarioDirectory = 'data/scenariosData/' + str(radius)
	global clustersFile
	clustersFile = 'data/scenariosData/' + str(radius) + '/clustering_' + str(radius) + '.json'
	global clusterFilename
	clusterFilename = 'data/scenariosData/' + str(radius) + '/clustering_' + str(radius) + '.json'
	global vehiclesDictFile
	vehiclesDictFile = 'data/scenariosData/' + str(radius) + '/vehiclesDict_' + str(numberOfVehicles) + '.json'
	global timesDictFile
	timesDictFile = 'data/scenariosData/' + str(radius) + '/timesDict_' + str(numberOfVehicles) + '_' + str(
		radius) + '.csv'

	global fwdGreedykDir
	fwdGreedykDir = 'data/solutions/fwdGreedy/k_' + str(k)
	global fwdGreedyFile
	fwdGreedyFile = 'data/solutions/fwdGreedy/k_' + str(k) + '/fwdGreedy_' + str(numberOfVehicles) + '_' + str(
		radius) + '.json'

	global backGreedykDir
	backGreedykDir = 'data/solutions/backGreedy/k_' + str(k)
	global backGreedyFile
	backGreedyFile = 'data/solutions/backGreedy/k_' + str(k) + '/backGreedy_' + str(numberOfVehicles) + '_' + str(
		radius) + '.json'

	global randomLocalSearchkDir
	randomLocalSearchkDir = 'data/solutions/randomLocalSearch/k_' + str(k)
	global randomLocalSearchFile
	randomLocalSearchFile = 'data/solutions/randomLocalSearch/k_' + str(k) + '/rndLocalSearch_' + str(
		numberOfVehicles) + '_' + str(radius) + '.json'
