class Parameters:
	def __init__(self): #Nof, Nov, Noz, Nos, scenarios, probabilities, beta, distances):
		self.Nof = 5							#Nof should be equal to |V| in G
		self.Nov = 3
		self.Noz = 4
		self.Nos = 3
		self.B = 400
		self.ps = [0.1, 0.6, 0.3]
		self.beta = [ [1, 2, 3, 0.1, 5.4], [4, 5, 6, 42, 12], [9, 4, 22, 34.2, 10] ]
		self.c = [10, 20, 30]																	# TO BE REMOVED	(length of this list as big as the #Nodes)
		self.cst = 12
		self.cr = 28
		self.R = 4
		self.gamma = 0.5