import itertools
import copy

def combinations(L, p):
	combs = []
	for subset in itertools.combinations(L, p):
		combs.append(list(subset))
	return combs


def isSwapFeasible(S, facilities, openfacIds, closedFacIds):
	totalSt, totalRap, totalCPs = 0, 0, 0
	openCPs = 0
	closedTotalCap = 0
	for facId in openfacIds:
		openCPs += S.y[facId]
	for facId in closedFacIds:
		for facility in facilities:
			if facility.id == facId:
				closedTotalCap += facility.capacity
	if closedTotalCap < openCPs:
		return False
	else:
		return True	


def swap(S, openFacIds, closedFacIds):
	newS = copy.deepcopy(S)
	openNewFacilities(newS)
	closeOldFacilities()


def openNewFacilities(newS, facilities, closedFacIds, standard, rapid, totalCPs):
	L = sorted(facilities, key=lambda x: x.capacity, reverse=True)
	for facility in L:
		facId = facility.id
		capacity = facility.capacity
		if rapid >= capacity:
			newS.r[facId] = capacity
			rapid -= capacity

			newS.st[facId] = 0
			
			newS.y[facId] = capacity
			totalCPs -= capacity
		
		elif rapid + standard >= capacity:
			newS.r[facId] = rapid
			rapid = 0
		
			remaining = capacity - rapid
			newS.st[facId] = remaining
			standard -= remaining
		
			newS.y[facId] = capacity
			totalCPs -= capacity

		elif rapid + standard < capacity:
			newS.r[facId] = rapid
			rapid = 0
		
			newS.st[facId] = standard
			standard = 0
		
			total = rapid + standard
			newS.y[facId] = total
			totalCPs -= total

	# sort the facilities in decreasing order of capacity in list L
	# get the first facility from L
	# add CPs until it is full
	# repeat for the rest of the facilities
	# if there are no more CPs to be added
	# do not open any other facility

def closeOldFacilities(S, openFacIds):
	for facId in openFacIds:
		S.close_facility(facId)

def getZoneNeighborhood(zone, parameters, S):
	neighborhood = []
	closedFacIds = []
	openFacIds = []
	newS = copy.deepcopy(S)
	for facility in zone.facilities:
		j = facility.id
		if S.is_open(j):
			openFacIds.append(j)
		else:
			closedFacIds.append(j)
	# if len(closedFacIds) < parameters.swaps or len(openFacIds) < parameters.swaps:
		# for swapLength in range(parameters.swaps):
		# 	openedComb = combinations(openedFacIds, swapLength)
		# 	for comb in openedComb:
		# 		for element in comb:
		# 			newS.close_facility(element)
		# 	closedComb = combinations(closedFacIds, swapLength)
		# 	for comb
	else:
		while 0:
			openFacCombList = combinations(openFacIds, parameters.swaps)
			closedFacCombList = combinations(closedFacIds, parameters.swaps)
			for openFacComb in openFacCombList:
				for closedFacComb in closedComb:
					for i in range(parameters.swaps):
						# facStandard, facRapid, facAllCPs = news.y[openFacComb[i]]
						# newS.close_facility(openFacComb[i])
						# newS.open_facility(closedFacComb[i])
						# standard += facStandard
						# rapid += facRapid
						# allFacilityCPs += facAllCPs
			
		# OPEN THE SAME NUMBER OF FACILITIES THAT WERE CLOSED IN THE NEW SOLUTION
		# ADD THE NEW SOLUTION TO THE LIST
		# KEEP A LIST OF NEW SOLUTIONS FOR EVERY ZONE
		# THEN CHECK IN THE LOCALSEARCH METHOD ALL THESE LISTS AND KEEP THE SOLUTION WITH THE BEST IMPROVEMENT
		# LATER DO THE GLOBAL NEIGHBORHOOD
		# generate scenqarios
	print("zoneClosedFacIds is ", zoneClosedFacIds)
	print("zoneOpenedFacIds is ", zoneOpenedFacIds)
	openedComb = combinations(zoneOpenedFacIds, parameters.swaps)
	print(openedComb)
	print("-----------")

def neighborhood(parameters, S, zones, distMatrix):
	old_cost = S.getCost(parameters, distMatrix)
	newS = copy.deepcopy(S)
	for zone in zones:
		getZoneNeighborhood(zone)
						



		

# def localSearch(S):
# 	neighborhood = getNeighborhood(S)
# 	flag = True
# 	while flag:
# 		for newSol in neighborhood:
# 			if newSol.getCost(parameters, distMatrix) < S.getCost(parameters, distMatrix):
# 				S = newSol



	# for every possible bundle of size p of closed facilities bunClFac
	# and for every bundle of opened facilities of size p (parameters.swaps)
	# check if the total capacity of all the facilities in the candidate bundle bunClFac
	# is at least as large as the number of CPs in the open facilities

	# for z in parameters.Noz:
	# 	closed = []
	# 	opened = []
	# 	for j in 


	
	# fl_to_open = combinations(closed, p)
	# fl_to_close = combinations(opened, p)
	# print("fl to open ", fl_to_open)
	# print("fl to close ", fl_to_close)
	# if fl_to_close:
	# 	tempS = solution(parameters)
	# 	for fl_tuple in fl_to_close:
	# 		for j in fl_tuple:

	# 		newS.close_facility(j)


	# print("opened is ", opened)
	# print("closed is ", closed)

	







# L = [1, 2, 3, 4]
# combs = combinations(L, 2)
# print(combs)
# parameters = pam.Parameters()
# S = sl.Solution(parameters)

# for j in range(parameters.Nof):
# 	facility = fl.facility(cost, capacity, alpha, zone)
# 	facilities.append(facility)

# neighborhood(parameters, S, 2)

# while there is a better solution

# get in a list all the possible combinations of swaps



# Make a simple data file with 3 rows for the facilities
# and another data file with 4 rows for the zones
# Then read the data from these files and create the objects above