import parameters as pam
import read_data as rdt
import network as nrk
import distMatrix as dmtx
import convertToAMPL as campl
import lagrangian as lag
import optimal as opt
import time


print("#########################################################\n#########################################################")
start_time = time.time()
parameters = pam.Parameters()

rdt.checkSizes(parameters)

parameters.getData()

G, weights = nrk.createNetwork()

parameters.getVehiclesAtRandomLocations(G)

parameters.distMatrix = dmtx.getDistMatrix(G, parameters.facilities, parameters.vehicles)

# ######### OPT solution ##############
campl.convertToAMPL(parameters)
instance, results = opt.solveOptimal()
optimalValue = opt.getOptimalValue(instance)
# opt.printOptimal(instance, results)

# ######### Approximate solution #####################
approximateValue = lag.lagrangian(parameters)

print("Approximation ratio: %f" %(approximateValue / optimalValue))
print("--- %s seconds ---" % (time.time() - start_time))











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