import initialise as intl
import parameters as pam
import read_data as rdt
import network as nrk
import distMatrix as dmtx
import local_search as ls
import convertToAMPL as campl
import lagrangian as lag
import redistribute as rdb
import optimal as opt


parameters = pam.Parameters()

rdt.checkSizes(parameters)

parameters.getData()

G, weights = nrk.createNetwork()

parameters.distMatrix = dmtx.getDistMatrix(G, weights, parameters.facilities, parameters.vehicles)

# ######### OPT solution ##############
campl.convertToAMPL(parameters)
opt.printOptimal()

# ######### Approximate solution #####################

# initSol = intl.initialise(parameters)
# ls.reduceCPs(parameters, initSol)
# for zone in parameters.zones:
#     zoneFacilities = zone.facilities
#     rdb.redistributeCPs(initSol, zoneFacilities)
# lag.lagrangian(initSol, parameters)
# newS = ls.localSearch(initSol, parameters)
# print("-------- AFTER LOCAL SEARCH ---------------")
# lag.lagrangian(newS, parameters)












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