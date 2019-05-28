# import parameters as pam
# import read_data as rdt
import importData as impdt
# import facility as fl
# import zone as zn
# import vehicle as vh
# import tripTimes as trtim
# import convertToAMPL as campl
# import lagrangian as lag
# import optimal as opt
import time
import preprocessing as pre
import initialise as intl
import solution as sl



if __name__ == "__main__":
	start_time = time.time()
	print("#########################################################\n#########################################################")
	pre.preprocessing(False)

	parameters = impdt.importNetworkAndDicts()
	# # S = sl.Solution(parameters)
	# # S.IsFeasibleWithBudget(parameters)
	S = intl.initialise(parameters,0)

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