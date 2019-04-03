import initialise as intl
import parameters as pam
import read_data as rdt
import network as nrk
import distMatrix as dmtx


parameters = pam.Parameters()

belonging = rdt.getBelongingList()
adjMatrix = rdt.getAdjMatrix()
facilities = rdt.getFacilities(belonging)
zones = rdt.getZones(facilities, adjMatrix)
vehicles = rdt.getVehicles()

G, weights = nrk.createNetwork()
distMatrix = dmtx.getDistMatrix(G, weights, facilities, vehicles)
initSol = intl.initialise(parameters, belonging, facilities, zones, distMatrix)

initSol.printSol(parameters, belonging, facilities, zones, distMatrix)


