import settings
from math import sin, cos, sqrt, atan2, radians
import _pickle as pickle
from random import choice
import sys
import time

def distanceInKm(latitude1, longitude1, latitude2, longitude2):
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


def nodeClustering(Gnx):
    toolbar_width = 40
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['

    candidateLocations = []
    N = pickle.loads(pickle.dumps(list(settings.parameters.facilitiesDict.keys()), -1))
    allNodesLength = len(settings.parameters.facilitiesDict.keys())
    while N:
        randomNode = choice(N)
        randomNodeLatitude = Gnx.nodes[randomNode]['pos'][0]
        randomNodeLongitude = Gnx.nodes[randomNode]['pos'][1]
        candidateLocations.append(randomNode)
        N.remove(randomNode)
        closeNodesToRemove = []
        for node in N:
            nodeLatitude = Gnx.nodes[node]['pos'][0]
            nodeLongitude = Gnx.nodes[node]['pos'][1]
            if distanceInKm(randomNodeLatitude, randomNodeLongitude, nodeLatitude, nodeLongitude) < settings.parameters.radius:
                closeNodesToRemove.append(node)
        for closeNode in closeNodesToRemove:
            N.remove(closeNode)
        percentage = (allNodesLength - len(N)) / allNodesLength * 100
        sys.stdout.write("%.2f %%" % percentage)
        sys.stdout.flush()
        time.sleep(0.1)
        if percentage >= 10:
            sys.stdout.write("\b" * 7)
        else:
            sys.stdout.write("\b" * 6)
        sys.stdout.flush()
    return candidateLocations










