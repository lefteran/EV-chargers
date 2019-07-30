
class Parameters:
	def __init__(self):
		self.facilitiesDict = {}
		self.zonesDict = {}
		self.belongingDict = {}
		self.adjacencyDict = {}
		self.vehiclesClosestTuples = {}
		self.removedFacilityIds = []

		self.vehiclesDict = {}
		self.timesDict = {}

		self.k = 50
		self.C = 1000
		self.r = 100
		self.p = 2
		self.radius = 0.1


class Flags:
	def __init__(self):
		self.importTimes = False
		self.useGraphTool = True
		self.parallelComputationOfTimes = True
		self.importVehiclesDict = False
		self.saveNetwork = True

def init():
	global parameters
	parameters = Parameters()
	global flags
	flags = Flags()