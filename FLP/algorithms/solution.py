import settings

class Solution:
	def __init__(self, L, cost, algorithm, time):
		self.solutionList = L
		self.cost = cost
		self.algorithm = algorithm
		self.time = time
		self.k = settings.parameters.k