
class Parameters:
	def __init__(self):
		self.vehiclesDict = {}
		self.timesDict = {}
		self.candidateLocations = []

		self.numberOfVehicles = 30
		self.radius = 0.1

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