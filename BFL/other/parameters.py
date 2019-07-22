# import read_data as rdt
# import random
# import vehicle as vcl

# class Parameters:
# 	def __init__(self): #Nof, Nov, Noz, Nos, scenarios, probabilities, beta, distances):
		# self.Nof = 6							#Nof should be equal to |V| in G
		# self.Nov = 3
		# self.Noz = 4
		# self.Nos = 3
		# self.B = 400
		# self.ps = [0.1, 0.6, 0.3]
		# self.beta = [ [1, 2, 3, 0.1, 5.4, 8], [4, 5, 6, 42, 12, 20], [9, 4, 22, 34.2, 10, 13] ]
		# self.c = [10, 20, 30, 16, 32, 46]																	# TO BE REMOVED	(length of this list as big as the #Nodes)
		# self.cst = 12
		# self.cr = 28
		# self.R = 4
		# self.gamma = 0.5
		# self.swaps = 2
		# self.lambdaMax = 10			# THIS NEEDS TO BE lambdaMax = max dist[i][j] check kulik schachnai paper
		# self.epsilon = 2

		# self.facilities = []
		# self.zones = []
		# self.vehicles = []
		# self.belonging = []
		# self.adjMatrix = []
		# self.distMatrix = []


	# def getData(self):
	# 	self.belonging = rdt.getBelongingList()
	# 	self.adjMatrix = rdt.getAdjMatrix()
	# 	self.facilities = rdt.getFacilities(self.belonging)
	# 	self.zones = rdt.getZones(self.facilities, self.adjMatrix)
		# self.vehicles = rdt.getVehicles()				# If we read vehicle data (locations) from a file

	# def getVehiclesAtRandomLocations(self, nodesLen):
	# 	for vehId in range(self.Nov):
	# 		locations = []
	# 		locations = [random.randint(1,nodesLen) for scenario in range(self.Nos)]
	# 		vehicle = vcl.Vehicle(vehId, locations)
	# 		self.vehicles.append(vehicle)

	
	# def getVehiclesAtRandomLocations(self, G):
	# 	edges = G.edges()
	# 	vehiclesLocations = []
	# 	for vehId in range(self.Nov):
	# 		locations = [[random.sample(edges, 1), random.uniform(0, 1)] for scenario in range(self.Nos)]
	# 		vehiclesLocations.append(locations)
	# 		vehicle = vcl.Vehicle(vehId, locations)
	# 		self.vehicles.append(vehicle)

	# 	########## DETERMINISTIC INPUT FOR DEBUGGING (comment below for random input) ##########
	# 	self.vehicles = []
	# 	# vehiclesLocations = [[[[(8, 16)], 0.1841314237047884], [[(23, 14)], 0.713438577667904], [[(11, 14)], 0.598855543617694]],\
	# 	# [[[(19, 17)], 0.48835321198895876], [[(8, 9)], 0.6478369013401375], [[(3, 12)], 0.8992587424601035]],\
	# 	# [[[(10, 17)], 0.5335953067269413], [[(7, 18)], 0.5939801822255262], [[(7, 18)], 0.14908187175492338]]]
	# 	vehiclesLocations = [[[[(18, 20)], 0.5564960348475084], [[(13, 24)], 0.06964220466962756], [[(22, 20)], 0.4261882559596851]],\
	# 	[[[(12, 13)], 0.720950178659288], [[(15, 14)], 0.46764388628758347], [[(3, 12)], 0.5572469484137]],\
	# 	[[[(10, 15)], 0.008096552852991157], [[(18, 20)], 0.25488543690567333], [[(19, 17)], 0.9108432659015407]]]
	# 	for vehId in range(self.Nov):
	# 		vehicle = vcl.Vehicle(vehId, vehiclesLocations[vehId])
	# 		self.vehicles.append(vehicle)
	# 	#######################################################################################

	# 	# print("random input locations", vehiclesLocations)