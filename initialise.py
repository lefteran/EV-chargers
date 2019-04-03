import read_data as rdt
import distMatrix as dmtx
import solution as sl
import parameters as pam
import copy

def initialise(parameters):
	S = sl.Solution(parameters)
	zones = rdt.getZones()
	facilities = rdt.getFacilities()
	distMatrix = dmtx.getDistMatrix()
	for z in range(parameters.Noz):
		Lz = copy.deepcopy(zones[z].facilities)
		if Lz:
			k = Lz[0].id			# get the first facility in Lz
			del Lz[0]
			S.open_facility(k)
			while S.y[k] < facilities[k].capacity and S.currentDemand(parameters, z) < parameters.gamma * zones[z].demand:
				if S.r[k] < parameters.R:
					S.r[k] += 1
					S.y[k] += 1
				else:
					S.st[k] += 1
					S.y[k] += 1
				if S.currentOnstreetCPs(parameters, z) == zones[z].onStreetBound:
					for element in Lz:
						if parameters.alpha[element] == 1:
							Lz.remove(element)
					try:
						k = Lz[0]
					except IndexError:
						print("No feasible solution for the problem (Nz)")
				if S.y[k] == facilities[k].capacity:
					try:
						k = Lz[0]
					except IndexError:
						print("No feasible solution for the problem (cap)")
					S.open_facility(k)
	for i in range(parameters.Nov):
		closest = distMatrix[i][0]
		closestFac = 0
		for j in range(parameters.Nof):
			if distMatrix[i][j] < closest:
				closest = distMatrix[i][j]
				closestFac = j
		S.connect(i, closestFac)
	print("Initial feasible solution")
	print("x is ", S.x)
	print("st is ", S.st)
	print("r is ", S.r)
	print("y is ", S.y)
	print("omega is ", S.omega)
	print("Cost of S is ", S.getCost(parameters))



parameters = pam.Parameters()
testSol = initialise(parameters)







# def lagrangian():



