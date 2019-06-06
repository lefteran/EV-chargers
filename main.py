import importData as impdt
import solution.lagrangian as lag
import time
import preprocessing as pre
import solution.solution as sl
import solution.initialise as intl



if __name__ == "__main__":
	start_time = time.time()
	print("#########################################################\n#########################################################")
	pre.preprocessing(False)

	parameters = impdt.importNetworkAndDicts()

	S, lagCost = lag.lagrangianRelaxation(True, parameters)
	cost = S.getCost(parameters)
	print("cost is %f" %cost)

	# CHECK WHETHER THERE IS A SOLUTION WITH FINITE COST. THEN COMPUTE COST BY DISCARDING inf VALUES.
	# SOLVE FIRST THE UNBUDGETED PROBLEM!!!!!!!!!!!!
	# INSTEAD OF A FOLDER SOLUTION CREATE TWO FOLDERS NAMED BUDGETED AND UNBUDGETED

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
