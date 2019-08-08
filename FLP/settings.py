import os

# ############################# Parameters #############################
facilitiesDict = {}
zonesDict = {}
belongingDict = {}
adjacencyDict = {}

vehiclesDict = {}
timesDict = {}

candidateLocations = []
numberOfVehicles = -1
radius = 0.2
iterations = -1

vehiclesClosestTuples = {}
removedFacilityIds = []
k = 50				# NUMBER OF FACILITIES TO BE OPENED
C = 1000
r = 1000			# NUMBER OF ITERATIONS FOR THE RANDOM LOCAL SEARCH
p = 1				# NUMBER OF FACILITIES TO SWAP (IN LS AND RANDOM LS)

algorithm = -1
algorithmDict = {0: "Optimal",
				 1: "Forward Greedy",
				 2: "Backward Greedy",
				 3: "Random Local Search",
				 4: "Local search"}

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
scenarioDirectory = ''
clustersFile = ''
clusterFilename = ''
vehiclesDictFile = ''
timesDictFile = ''


optimalDir = ''
# optimalDataFile = 'data/timesDictTest.dat'
optimalDataFile = ''
# optimalMapping = 'data/scenariosData/' + str(radius) + '/optimalMapping_' + str(numberOfVehicles) + '_' + str(radius) + '.json'
optimalMapping = ''
optimalSolutionFile = ''

fwdGreedykDir = ''
fwdGreedyFile = ''

backGreedykDir = ''
backGreedyFile = ''

randomLocalSearchkDir = ''
randomLocalSearchFile = ''

localSearchkDir = ''
localSearchFile = ''



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

	global optimalDir
	optimalDir = 'data/solutions/optimal/k_' + str(k)
	global optimalDataFile
	optimalDataFile = os.path.abspath(
		'D:\Github\EV-chargers\FLP\data\scenariosData\\' + str(radius) + '\\timesDict_' + str(numberOfVehicles) + '_' + str(
		radius) + '.dat')
	global optimalMapping
	optimalMapping = 'D:\Github\EV-chargers\FLP\data\scenariosData\\' + str(radius) + '\optimalMapping_' + str(numberOfVehicles) + '_' + str(radius) + '.json'
	global optimalSolutionFile
	optimalSolutionFile = 'data/solutions/optimal/k_' + str(k) + '/optimal_' + str(numberOfVehicles) + '_' + str(
		radius) + '.json'

	global fwdGreedykDir
	fwdGreedykDir = 'data/solutions/fwdGreedy/k_' + str(k)
	global fwdGreedyFile
	fwdGreedyFile = 'data/solutions/fwdGreedy/k_' + str(k) + '/' + str(radius) + '/fwdGreedy_' + str(numberOfVehicles) + '_' + str(
		radius) + '.json'

	global backGreedykDir
	backGreedykDir = 'data/solutions/backGreedy/k_' + str(k)
	global backGreedyFile
	backGreedyFile = 'data/solutions/backGreedy/k_' + str(k) + '/backGreedy_' + str(numberOfVehicles) + '_' + str(
		radius) + '.json'

	global randomLocalSearchkDir
	randomLocalSearchkDir = 'data/solutions/randomLocalSearch/k_' + str(k) + '/p_' + str(p) + '/r_' + str(r) + '/run_'
	global randomLocalSearchFile
	randomLocalSearchFile = 'data/solutions/randomLocalSearch/k_' + str(k)  + '/p_' + str(p) + '/r_' + str(r) + '/run_' \
		+ '/rndLocalSearch_' + str(numberOfVehicles) + '_' + str(radius) + '.json'

	global localSearchkDir
	localSearchkDir = 'data/solutions/localSearch/k_' + str(k)
	global localSearchFile
	localSearchFile = 'data/solutions/localSearch/k_' + str(k) + '/localSearch_' + str(
		numberOfVehicles) + '_' + str(radius) + '.json'



def setNumberOfVehicles(number):
	global numberOfVehicles
	numberOfVehicles = number

def setAlgorithm(number):
	global algorithm
	algorithm = number


def resetNumberOfIterations(numberOfIterations):
	global iterations
	iterations = numberOfIterations


def resetRandomLocalSearchkDir(iteration):
	global randomLocalSearchkDir
	randomLocalSearchkDir += str(iteration)

def resetRandomLocalSearchFile(iteration):
	global randomLocalSearchFile
	randomLocalSearchFile = 'data/solutions/randomLocalSearch/k_' + str(k) + '/p_' + str(p) + '/r_' + str(r) + '/run_' + str(iteration)\
							+ '/rndLocalSearch_' + str(numberOfVehicles) + '_' + str(radius) + '.json'