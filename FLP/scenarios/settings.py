
class Parameters:
	def __init__(self):
		# self.facilitiesDict = {}
		# self.zonesDict = {}
		# self.belongingDict = {}
		# self.adjacencyDict = {}
		#
		self.vehiclesDict = {}
		self.timesDict = {}
		#
		# self.standardCost = 25
		# self.rapidCost = 38
		# self.budget = 400000000
		#
		# self.gamma = 0.5
		# self.R = 10
		# self.lambdaMax = 10
		# self.epsilon = 2
		# self.swaps = 2


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