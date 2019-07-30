import matplotlib.cm as cm
import matplotlib.colors as colors
import networkx as nx
import settings
import osmnx as ox
import pandas as pd
import saveLoadNetwork
# %matplotlib inline


def visualiseNetwork(networkName):
    ox.config(log_console=True, use_cache=True)

    if not settings.flags.saveNetwork:
        G = saveLoadNetwork.loadNetwork('Piedmont.graphml')
    else:
        G = ox.graph_from_place(networkName, network_type='drive')
        G = ox.project_graph(G)

    # fig, ax = ox.plot_graph(G, bgcolor='k', node_size=30, node_color='#999999', node_edgecolor='none', node_zorder=2,
    #                         edge_color='#555555', edge_linewidth=1.5, edge_alpha=1)
    #
    #
    # # node closeness centrality
    # node_centrality = nx.closeness_centrality(G)
    #
    # # plot it
    # df = pd.DataFrame(data=pd.Series(node_centrality).sort_values(), columns=['cc'])
    # df['colors'] = ox.get_colors(n=len(df), cmap='inferno', start=0.2)
    # df = df.reindex(G.nodes())
    # nc = df['colors'].tolist()
    # fig, ax = ox.plot_graph(G, bgcolor='k', node_size=30, node_color=nc, node_edgecolor='none', node_zorder=2,
    #                         edge_color='#555555', edge_linewidth=1.5, edge_alpha=1)
    return G











