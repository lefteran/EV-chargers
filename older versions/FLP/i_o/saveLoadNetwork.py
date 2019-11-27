import osmnx as ox

def saveNetwork(G, filename):
    ox.save_graphml(G, filename = filename)


def loadNetwork(filename):
    G = ox.load_graphml(filename)
    return G