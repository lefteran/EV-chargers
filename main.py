import importData as impdt
import solution.unbudgeted as unbu
import solution.lagrangian as lag
import time
# import preprocessing as pre
import Parameters
import serialization
import exportCosts
import solution.solution as sl
import solution.initialise as intl
import unittest
# import unitTests.test_Times as test_Times


if __name__ == "__main__":
	start_time = time.time()
	print("#########################################################\n#########################################################")
	parameters = Parameters.Parameters()

	####################### PREPROCESSING #####################################
	# pre.preprocessing(parameters.doPreprocessing)

	########################## IMPORTING NETWORK (G, facilities and zones) ###########################################
	print("Importing network ...")
	Gnx = impdt.importNetwork(parameters)
	if parameters.importTimes:
		GtNetwork = None
	else:
		import GraphToolNetwork as gtn
		GtNetwork = gtn.GraphToolNetwork()
		GtNetwork.createGraphToolNetworkFromGnx(Gnx)
	########################## GET VEHICLES AND COMPUTE VEHICLE-FACILITY DISTANCES ###################################
	print("Getting vehicles and vehicle-facility times ...")
	impdt.getVehicles(Gnx, parameters)
	impdt.getTimes(Gnx, GtNetwork, parameters)

	####################### TESTING #####################################
	# suite = unittest.TestLoader	().loadTestsFromModule(test_Times)
	# unittest.TextTestRunner(verbosity=2).run(suite)

	####################### MAIN ALGORITHM #####################################
	# initSol = intl.initialiseSolution(parameters)
	# localSearchSolution = serialization.importAndDeserialize('Chicago/unbudgetedLocalSearchSolution' + str(parameters.swaps) + 'Swaps.json')
	# initialSolutionCost = initSol.getLagrangianCost(parameters, 0)
	# localSearchSolutionCost = localSearchSolution.getLagrangianCost(parameters, 0)
	# print(f"Initial cost: {initialSolutionCost}. Local search cost: {localSearchSolutionCost}. Number of swaps: {parameters.swaps}\n")
	initialSolution, localSearchSolution = unbu.getUnbudgetedSolution(parameters)
	initialSolutionCost = initialSolution.getCost(parameters)
	localSearchSolutionCost = localSearchSolution.getCost(parameters)
	serialization.serializeAndExport(localSearchSolution, 'Chicago/unbudgetedLocalSearchSolution' + str(parameters.swaps) + 'Swaps.json')
	exportCosts.exportCosts('Chicago/solutionsCosts.txt', parameters, initialSolutionCost, localSearchSolutionCost)

	# WRITE THE COSTS OF THE INITIAL SOLUTION AND THE COST OF THE SOLUTION FROM LOCAL SEARCH IN A FILE

	# initSol = serialization.importAndDeserialize('Chicago/initialSolution.json')
	# initSolCost = initSol.getCost(parameters)
	# sol = serialization.importAndDeserialize('Chicago/localSearchSolution2Swaps.json')
	# solCost = sol.getCost(parameters)
	# print(f"Initial cost is {initSolCost} and after local search the cost is {solCost}")


	# cost = S.getCost(parameters)


	# S, lagCost = lag.lagrangianRelaxation(True, parameters)
	# print("cost is %f" %cost)

	print("--- %s seconds ---" % (time.time() - start_time))










############################## OLD MAIN ################################
# rdt.checkSizes(parameters)

	# parameters.getData()

	# G, weights = impdt.createNetwork()

	# parameters.getVehiclesAtRandomLocations(G)

	# parameters.distMatrix = dmtx.getDistMatrix(G, parameters.facilities, parameters.vehicles)

	# # ######### OPT solution ##############
	# campl.convertToAMPL(parameters)
	# instance, results = opt.solveOptimal()
	# optimalValue = opt.getOptimalValue(instance)
	# # opt.printOptimal(instance, results)

	# # ######### Approximate solution #####################
	# approximateValue = lag.lagrangian(parameters)

	# print("Approximation ratio: %f" %(approximateValue / optimalValue))

# T = []
# for facility in parameters.facilities:
#     T.append(facility.capacity)
#     print("T: id is %d and capacity is %d" %(facility.id, facility.capacity))
# # print("T is ",T)

# Lcap = sorted(parameters.facilities, key=lambda x: x.capacity, reverse=True)
# for facility in Lcap:
#     T.append(facility.capacity)
#     print("Lcap: id is %d and capacity is %d" %(facility.id, facility.capacity))
# # print("Lcap is ", Lcap)


# for i in range(len(initSol.y)):
#     print("Unsorted y: y[%d] = %d" %(i, initSol.y[i]))

# Ly = sorted(range(len(initSol.y)), key=lambda k: initSol.y[k])

# for index in Ly:
#     print("Sorted y: y[%d] = %d" %(index, initSol.y[index]))

# print("Indices of Ly are ", Ly)

# Ly = sorted(initSol, key=lambda x: x.y, reverse=False)

# ls.neighborhood(parameters, initSol, parameters.zones, distMatrix)



# from shapely.geometry import Point, LineString
# for node in G.nodes_iter():
#     if G.degree(node) > 2:
#         print Point(node) #the nodes
#         for edge in G.edges(node):
#             print LineString(edge) # the edges (>2)


# print(G.edges(1))			# print edges adjacent to node 1


# https://stackoverflow.com/questions/10052912/how-to-sort-dictionaries-of-objects-by-attribute-value-in-python
