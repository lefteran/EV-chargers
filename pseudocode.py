def globalLocalSearch():
	




def localSearch(S):
	# zonesFlags = [True] * parameters.Noz		# if the flag of a zone is False no further 
												# improvements are possible for that zone
												# for the chosen value of paramters.swap
	# while there is an improved solution i.e. flag==True
		# curZoneId = 0
		# for zone in zones
			# open, closed = getOpenAndClosedFacIds()
			# for each possible combination of swaps:
				# newS = getCandidateSolution()		
				# if newS improves the cost 
					# set S=newS
					# break
			# zonesFlags[zone.id] = False
			# break
		# set flag=False (at the end of zones for loop)


	# move on to the next zone and mark the previous one as red (i.e. no further improvement)
	# if there no improving solution from any of the zones
	# check if the number of CPs can be decreased and then
	# return the latest solution

def getOpenAndClosedFacIds(zone):


def distributeCPs				# distribute the CPs accross facilities


def getSolWithClosedFacs(S, facilities):
	# for fac in facilities
		# if the CPs of fac can reduced
			# reduce CPs of fac
		# sort facilities in each zone in list Lcap with decreasing order of cap
		# sort facilities in each zone in Ly with increasing order of y

		# redistrubute the CPs to those facilities with largest caps

		# if isFeasible(S.close_facility(fac))
			# S.close_facility(fac)
		# checkCPs()

def checkCPs(newS):					# pre local search improvement
	# for every open facility in newS check if 
	# the number of charging points can be decreased
	# by maintaining feasibility


def getCandidateSolution():
# IF ALL THE FACILITIES ARE OPEN TRY TO CLOSE parameters.swaps FACILITIES
	# IF THE SOLUTION IS FEASIBLE THEN PROCEED OTHERWISE TRY TO CLOSE FEWER FACILITIES
	# THEN DECREASE THE parameters.swaps NUMBER AND PERFORM LOCAL SEARCH 
# else:
	# let comb be a combination of sets set1 and set2 to swap
	# if isSwapFeasible():
		# newS = swap() 			
		# returns newS










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

# def neighborhood(parameters, S, zones, distMatrix):
# 	old_cost = S.getCost(parameters, distMatrix)
# 	newS = copy.deepcopy(S)
# 	for zone in zones:
# 		getZoneNeighborhood(zone)
						