import parameters as pam
import networkx as nx

def getDistMatrix(G, weights, facilities, vehicles):
    parameters = pam.Parameters()
    distMatrix = [ [0] * parameters.Nof ] * parameters.Nov
    for i in range(parameters.Nov):
        vclLocationList = vehicles[i].location
        for j in range(parameters.Nof):
            facLocation = facilities[j].location
            expDist = 0
            for scenario in range(len(vclLocationList)):
                vclLocation = vclLocationList[scenario]
                dist = parameters.beta[i][j] * parameters.ps[scenario] * nx.shortest_path_length(G, source=vclLocation, target=facLocation, weight='weight')
                expDist += dist
            distMatrix[i][j] = expDist
    return distMatrix


# distMatrix = getDistMatrix()
# print(distMatrix)