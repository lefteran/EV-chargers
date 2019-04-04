import initialise as intl
import parameters as pam
import read_data as rdt
import network as nrk
import distMatrix as dmtx
import local_search as ls


parameters = pam.Parameters()

rdt.checkSizes(parameters)

belonging = rdt.getBelongingList()
adjMatrix = rdt.getAdjMatrix()
facilities = rdt.getFacilities(belonging)
zones = rdt.getZones(facilities, adjMatrix)
vehicles = rdt.getVehicles()

G, weights = nrk.createNetwork()
# nrk.plotNetwork(G)
distMatrix = dmtx.getDistMatrix(G, weights, facilities, vehicles)
initSol = intl.initialise(parameters, belonging, facilities, zones, distMatrix)

initSol.printSol(parameters, belonging, facilities, zones, distMatrix)

ls.neighborhood(parameters, initSol, zones, distMatrix)