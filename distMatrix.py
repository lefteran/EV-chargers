import read_data as rdt
import parameters as pam
import networkx as nx
import network as nrk

def getDistMatrix():
    parameters = pam.Parameters()
    G, weights = nrk.createNetwork()
    distMatrix = [ [0] * parameters.Nof ] * parameters.Nov
    vehicleList = rdt.getVehicles()
    facilityList = rdt.getFacilities()
    for i in range(parameters.Nov):
        vclLocationList = vehicleList[i].location
        for j in range(parameters.Nof):
            facLocation = facilityList[j].location
            expDist = 0
            for scenario in range(len(vclLocationList)):
                vclLocation = vclLocationList[scenario]
                dist = parameters.beta[i][j] * parameters.ps[scenario] * nx.shortest_path_length(G, source=vclLocation, target=facLocation, weight='weight')
                expDist += dist
            distMatrix[i][j] = expDist
    return distMatrix


# distMatrix = getDistMatrix()
# print(distMatrix)