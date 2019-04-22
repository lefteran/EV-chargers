import parameters as pam
import networkx as nx
from math import sin, cos, sqrt, atan2, radians

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


def getDistMatrixFromEdgePoints(G, weights, facilities, vehicles):
    parameters = pam.Parameters()
    distMatrix = [ [0] * parameters.Nof ] * parameters.Nov
    for i in range(parameters.Nov):
        vclLocationList = vehicles[i].location
        for j in range(parameters.Nof):
            facLocation = facilities[j].location
            expDist = 0
            for scenario in range(len(vclLocationList)):
                vclLocation = vclLocationList[scenario]
                edgeLocation = vclLocation[0][0]
                edgePoint = vclLocation[1]
                edgeOrigin = edgeLocation[0]
                edgeDestination = edgeLocation[1]
                edgeWeight = G[edgeOrigin][edgeDestination]['weight']
                
                distance1 = edgeWeight * edgePoint + parameters.beta[i][j] * parameters.ps[scenario] *\
                nx.shortest_path_length(G, source=edgeOrigin, target=facLocation, weight='weight')

                distance2 = edgeWeight * (1 - edgePoint) + parameters.beta[i][j] * parameters.ps[scenario] *\
                nx.shortest_path_length(G, source=edgeDestination, target=facLocation, weight='weight')

                dist = min(distance1, distance2)
                expDist += dist
            distMatrix[i][j] = expDist
    return distMatrix




def calculateDistanceInKm(latitude1, longitude1, latitude2, longitude2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(latitude1)
    lon1 = radians(longitude1)
    lat2 = radians(latitude2)
    lon2 = radians(longitude2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance






# latitude1 = 43.6128279174
# longitude1 = -96.7704197366
# latitude2 = 43.5293061262
# longitude2 = -96.7510354923
# calculateDistance(latitude1, longitude1, latitude2, longitude2)


# distMatrix = getDistMatrix()
# print(distMatrix)
