import matplotlib.cm as cm
import matplotlib.colors as colors
import networkx as nx
import settings
import osmnx as ox
import pandas as pd
import i_o.saveLoadNetwork as saveLoadNetwork
import i_o.serializationIO as serializationIO
from random import uniform
# %matplotlib inline


def plotGraph(G):
    fig, ax = ox.plot_graph(G, bgcolor='k', node_size=3, node_color='#999999', node_edgecolor='none', node_zorder=2,
                            edge_color='#555555', edge_linewidth=0.5, edge_alpha=1)

def visualiseNodes(G, nodesDict, place):
    # node closeness centrality - a node dict
    # node_centrality = nx.closeness_centrality(G)

    # plot it
    # df = pd.DataFrame(data=pd.Series(nodesDict).sort_values(), columns=['cc'])
    # df['colors'] = ox.get_colors(n=len(df), cmap='inferno', start=0.2)
    # df = df.reindex(G.nodes())
    # nc = df['colors'].tolist()

    # clusterFilename = 'clustering_0.1.json'
    cluster = serializationIO.importAndDeserialize(settings.clusterFilename)
    candidateLocations = cluster['candidateLocations']

    # solObject = serializationIO.importAndDeserialize("fwdGreedy_50_0.1.json")
    solObject = serializationIO.importAndDeserialize(settings.localSearchFile)
    solutionList = solObject.solutionList

    nc = []
    ns = []
    # candidatesCoordinates = []
    # solutionCoordinates = []
    for node, data in G.nodes(data=True):
        if str(node) in solutionList:
            nc.append('#F1E443')
            ns.append(10)
            # solutionCoordinates.append((G.nodes[node]['lat'], G.nodes[node]['lon']))
        elif str(node) in candidateLocations:
            nc.append('b')
            ns.append(2.5)
            # candidatesCoordinates.append((G.nodes[node]['lat'], G.nodes[node]['lon']))
        else:
            # nc.append('b')
            # nc.append('#00ffff')
            nc.append('None')
            # ns.append(0.7)
            ns.append(0)

    # serializationIO.serializeAndExport(solutionCoordinates, 'data/solutionCoordinates.json')
    # serializationIO.serializeAndExport(candidatesCoordinates, 'data/candidatesCoordinates.json')

    fig, ax = ox.plot_graph(G, bgcolor='#CFCCCB', node_size=ns, node_color=nc, node_edgecolor='none', node_zorder=2,
                            edge_color='#555555', edge_linewidth=0.3, edge_alpha=1, dpi=500)
    fig.savefig('figures/' + place + 'qiming.png', #facecolor=fig.get_facecolor(),
    dpi=300)

def visualiseEdges(G, edgesDict):
    # edge_centrality = nx.closeness_centrality(nx.line_graph(G))
    # list of edge values for the orginal graph
    edgesColouredList = [edgesDict[edge] for edge in G.edges()]

    # color scale converted to list of colors for graph edges
    norm = colors.Normalize(vmin=min(edgesColouredList) * 0.8, vmax=max(edgesColouredList))
    cmap = cm.ScalarMappable(norm=norm, cmap=cm.inferno)
    ec = [cmap.to_rgba(cl) for cl in edgesColouredList]

    # color the edges in the original graph with closeness centralities in the line graph
    fig, ax = ox.plot_graph(G, bgcolor='k', axis_off=True, node_size=0, node_color='w', node_edgecolor='gray',
                            node_zorder=2,
                            edge_color=ec, edge_linewidth=1.5, edge_alpha=1)


def visualiseNetwork(networkName, filename, place):
    ox.config(log_console=True, use_cache=True)

    if not settings.saveNetwork:
        G = saveLoadNetwork.loadNetwork('osmFiles/' + filename)
    else:
        G = ox.graph_from_place(networkName, network_type='drive')
        G = ox.project_graph(G)

    # edgesDict = {}
    #
    # for edge in G.edges():
    #     edgesDict[edge] = uniform(0, 1)


    nodesDict = {}
    count = 0
    for node in G.nodes():
        count += 1
        if count <= 100:
            nodesDict[node] = 0
        else:
            nodesDict[node] = 1
    visualiseNodes(G, nodesDict, place)
    # plotGraph(G)
    # illustrateNodeCentrality(G)
    # illustrateEdgeCentrality(G, edgesDict)
    return G













