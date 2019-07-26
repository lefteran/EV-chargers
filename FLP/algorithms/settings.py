
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

		self.k = 10
		self.C = 1000


class Flags:
	def __init__(self):
		self.importTimes = False
		self.useGraphTool = True
		self.parallelComputationOfTimes = True
		self.importVehiclesDict = False

def init():
	global parameters
	parameters = Parameters()
	global flags
	flags = Flags()