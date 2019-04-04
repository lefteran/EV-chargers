import solution as sl
import parameters as pam
import copy



def initialise(parameters, belonging, facilities, zones, distMatrix):
	S = sl.Solution(parameters)
	for zone in zones:
		z = zone.id
		for facility in zone.facilities:
			if facility.alpha == 0:								# open off-street facilities first
				k = facility.id
				while S.y[k] < facility.capacity:
					installCP(parameters.R, S, k)
	for zone in zones:
		z = zone.id
		for facility in zone.facilities:
			if facility.alpha == 1:								# open on-street facilities
				k = facility.id
				if S.zoneOnstreetCPs(zone.facilities) < zone.onStreetBound:
					while (S.y[k] < facility.capacity) and (S.zoneOnstreetCPs(zone.facilities) < zone.onStreetBound):
						installCP(parameters.R, S, k)
	for i in range(parameters.Nov):
		closest = distMatrix[i][0]
		closestFac = 0
		for j in range(parameters.Nof):
			if distMatrix[i][j] < closest:
				closest = distMatrix[i][j]
				closestFac = j
		S.connect(i, closestFac)
	return S


def installCP(R, S, k):
	if sum(S.r) < R:
		S.r[k] += 1
	else:
		S.st[k] += 1
	S.y[k] += 1






# def initialise(parameters, belonging, facilities, zones, distMatrix):
# 	S = sl.Solution(parameters)
# 	for z in range(parameters.Noz):
# 		Lz = copy.deepcopy(zones[z].facilities)			# Lz in pseudocode facilitiesinZone
# 		if Lz:
# 			k = Lz[0].id			# get the first facility in Lz
# 			del Lz[0]
# 			S.open_facility(k)
# 			while S.y[k] < facilities[k].capacity and S.currentDemand(parameters, zones, z) < parameters.gamma * zones[z].demand:
# 				if S.r[k] < parameters.R:
# 					S.r[k] += 1
# 					S.y[k] += 1
# 				else:
# 					S.st[k] += 1
# 					S.y[k] += 1
# 				if S.currentOnstreetCPs(parameters, facilities, belonging, z) == zones[z].onStreetBound:
# 					for element in Lz:
# 						if parameters.alpha[element] == 1:
# 							Lz.remove(element)
# 					try:
# 						k = Lz[0]
# 					except IndexError:
# 						print("No feasible solution for the problem (Nz)")
# 				if S.y[k] == facilities[k].capacity:
# 					try:
# 						k = Lz[0]
# 					except IndexError:
# 						print("No feasible solution for the problem (cap)")
# 					S.open_facility(k)
# 	for i in range(parameters.Nov):
# 		closest = distMatrix[i][0]
# 		closestFac = 0
# 		for j in range(parameters.Nof):
# 			if distMatrix[i][j] < closest:
# 				closest = distMatrix[i][j]
# 				closestFac = j
# 		S.connect(i, closestFac)
# 	return S


# parameters = pam.Parameters()
# testSol = initialise(parameters)


# print("Initial feasible solution")
# print("x is ", testSol.x)
# print("st is ", testSol.st)
# print("r is ", testSol.r)
# print("y is ", testSol.y)
# print("omega is ", testSol.omega)
# print("Cost of testSol is ", testSol.getCost(parameters))
# print("Solution feasible: %r" %testSol.isFeasible(parameters))





# def lagrangian():



