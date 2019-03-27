class Parameters:
	def __init__(self): #Nof, Nov, Noz, Nos, scenarios, probabilities, beta, distances):
		self.Nof = 3
		self.Nov = 2
		self.Noz = 4
		self.Nos = 2
		self.B = 400
		self.ps = [0.2, 0.8]
		self.beta = [ [1, 2, 3], [4, 5, 6] ]
		self.c = [10, 20, 30]
		self.cst = 12
		self.cr = 28
		self.R = 4
		self.cap = [10, 20, 16]
		self.alpha = [0, 0, 1]
		self.gamma = 0.5
		self.H = [ [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0] ]
		self.A = [ [1, 1, 1, 0], [1, 1, 1, 0], [1, 1, 1, 0], [0, 1, 1, 1] ]
		self.Nz = [10, 15 ,19, 23]
		self.demand = [10, 13, 9, 17]
		self.dist = [  [ [0.1, 0.2, 0.3], [0.4, 0.5, 0.6] ],\
					   [ [0.7, 0.8, 0.9], [1.0, 1.2, 1.3] ]]		# scenario 2

		# Check if the parameter arrays have the correct sizes
		if len(self.beta) != self.Nov or len(self.beta[0]) != self.Nof or len(self.ps) != self.Nos \
		or len(self.dist) != self.Nos or len(self.dist[0]) != self.Nov or len(self.dist[0][0]) != self.Nof\
		or len(self.c) != self.Nof or len(self.cap) != self.Nof or len(self.H) != self.Nof\
		or len(self.H[0]) != self.Noz or len(self.Nz) != self.Noz or len(self.A) != self.Noz\
		or len(self.A[0]) != self.Noz:
			print("*** Incorrect size in the arrays of parameters ***")