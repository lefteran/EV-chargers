import initialise as intl
import parameters as pam
import read_data as rdt
import network as nrk
import distMatrix as dmtx
import local_search as ls
import convertToAMPL as campl


parameters = pam.Parameters()

rdt.checkSizes(parameters)

belonging = rdt.getBelongingList()
adjMatrix = rdt.getAdjMatrix()
facilities = rdt.getFacilities(belonging)
zones = rdt.getZones(facilities, adjMatrix)
vehicles = rdt.getVehicles()

G, weights = nrk.createNetwork()

distMatrix = dmtx.getDistMatrix(G, weights, facilities, vehicles)

# ######### OPT solution ##############
# print(adjMatrix)
# campl.convertToAMPL(facilities, zones, vehicles, belonging, adjMatrix)

# ######### Approximate solution
initSol = intl.initialise(parameters, belonging, facilities, zones, distMatrix)

initSol.printSol(parameters, belonging, facilities, zones, distMatrix)

ls.neighborhood(parameters, initSol, zones, distMatrix)