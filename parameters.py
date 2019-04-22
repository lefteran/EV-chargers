import read_data as rdt
import random
import vehicle as vcl

class Parameters:
	def __init__(self): #Nof, Nov, Noz, Nos, scenarios, probabilities, beta, distances):
		self.Nof = 6							#Nof should be equal to |V| in G
		self.Nov = 3
		self.Noz = 4
		self.Nos = 3
		self.B = 400
		self.ps = [0.1, 0.6, 0.3]
		self.beta = [ [1, 2, 3, 0.1, 5.4, 8], [4, 5, 6, 42, 12, 20], [9, 4, 22, 34.2, 10, 13] ]
		self.c = [10, 20, 30, 16, 32, 46]																	# TO BE REMOVED	(length of this list as big as the #Nodes)
		self.cst = 12
		self.cr = 28
		self.R = 4
		self.gamma = 0.5
		self.swaps = 2
		self.lambdaMax = 100000000			# THIS NEEDS TO BE lambdaMax = max dist[i][j] check kulik schachnai paper

		self.facilities = []
		self.zones = []
		self.vehicles = []
		self.belonging = []
		self.adjMatrix = []
		self.distMatrix = []


	def getData(self):
		self.belonging = rdt.getBelongingList()
		self.adjMatrix = rdt.getAdjMatrix()
		self.facilities = rdt.getFacilities(self.belonging)
		self.zones = rdt.getZones(self.facilities, self.adjMatrix)
		# self.vehicles = rdt.getVehicles()				# If we read vehicle data (locations) from a file

	# the location of a vehicle should be not only on a node of G but at some (random) point of any edge
	def getVehiclesAtRandomLocations(self, nodesLen):
		for vehId in range(self.Nov):
			locations = []
			locations = [random.randint(1,nodesLen) for scenario in range(self.Nos)]
			vehicle = vcl.Vehicle(vehId, locations)
			self.vehicles.append(vehicle)

	
	def getVehiclesAtRandomLocations1(self, G):
		edges = G.edges()
		vehiclesLocations = []
		for vehId in range(self.Nov):
			locations = [[random.sample(edges, 1), random.uniform(0, 1)] for scenario in range(self.Nos)]
			vehiclesLocations.append(locations)
			vehicle = vcl.Vehicle(vehId, locations)
			self.vehicles.append(vehicle)