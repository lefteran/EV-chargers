import itertools
import copy

def combinations(L, p):
	combs = []
	for subset in itertools.combinations(L, p):
		combs.append(list(subset))
	return combs

# p parameter of the swaping elements
def neighborhood(parameters, S, zones, distMatrix):
	old_cost = S.getCost(parameters, distMatrix)
	newS = copy.deepcopy(S)
	for zone in zones:
		zoneClosedFacIds = []
		zoneOpenedFacIds = []
		for facility in zone.facilities:
			j = facility.id
			if S.is_open(j):
				zoneOpenedFacIds.append(j)
			else:
				zoneClosedFacIds.append(j)
		print("zoneClosedFacIds is ", zoneClosedFacIds)
		print("zoneOpenedFacIds is ", zoneOpenedFacIds)
		openedComb = combinations(zoneOpenedFacIds, parameters.swaps)
		print(openedComb)
		print("-----------")

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