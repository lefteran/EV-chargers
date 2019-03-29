import solution as sl
import generalFuncs as gn

def initialise(parameters):
	S = sl.Solution(parameters)
	for z in range(parameters.Noz):
		Lz = []
		for j in range(parameters.Nof):
			if parameters.H[j][z] == 1:
				Lz.append(j)
		if Lz:
			k = Lz[0]			# k is the number of a facility
			del Lz[0]
			S.open_facility(k)
			while S.y[k] < parameters.cap[k] and\
			gn.currentDemand(parameters, S, z) < parameters.gamma * parameters.demand[z]:
				if S.r[k] < parameters.R:
					S.r[k] += 1
					S.y[k] += 1
				else:
					S.st[k] += 1
					S.y[k] += 1
				if gn.currentOnstreetCPs(parameters, S, z) == parameters.Nz[z]:
					for element in Lz:
						if parameters.alpha[element] == 1:
							Lz.remove(element)
					try:
						k = Lz[0]
					except IndexError:
						print("No feasible solution for the problem (Nz)")
				if S.y[k] == parameters.cap[k]:
					try:
						k = Lz[0]
					except IndexError:
						print("No feasible solution for the problem (cap)")
					S.open_facility(k)
	for i in range(parameters.Nov):
		closestFac = 0
		closestDist = 0
		for j in range(parameters.Nof):
			avg_dist = 0
			for s in range(parameters.Nos):
				avg_dist += parameters.ps[s] * parameters.dist[s][i][j]
			if avg_dist < closestDist:
				closestFac = j
		S.x[i][closestFac] = 1
	print("Initial feasible solution")
	print("x is ", S.x)
	print("st is ", S.st)
	print("r is ", S.r)
	print("y is ", S.y)
	print("omega is ", S.omega)
	print("Cost of S is ", S.cost(parameters))











# def lagrangian():



