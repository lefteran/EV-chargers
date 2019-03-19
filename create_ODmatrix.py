# Create OD matrix for the distances of each driver to every facility (nodes of the network) under one scenario
# The location of each driver is set to be the middle of an edge which is selected under some probability

import networkx as nx
from numpy.random import choice
import itertools
import matplotlib.pyplot as plt
import create_network as cn


def create_ODmatrix(driversNo):
	dLocations=[0]*driversNo
	G, weights = cn.create_network()
	dist = [[0 for i in range(len(list(G.nodes())))] for j in range(driversNo)]

	probabilities = []
	edgesNum = len(G.edges())
	for i in range(edgesNum):
		probabilities.append(1.0 / float(edgesNum))

	nodeList=list(G.nodes())
	edgeList=list(G.edges())
	E=range(edgesNum)
	for i in range(driversNo):
		draw = int(choice(E,1,probabilities))
		dLocations[i]=draw

	for i in range(driversNo):
		for j in range(len(G.nodes())):
			edge=edgeList[dLocations[i]]
			endpoints=list(itertools.chain(*[edge]))
			endpoint1=endpoints[0]
			endpoint2=endpoints[1]
			half_edge_weight=float(G[endpoint1][endpoint2]['weight'])/2
			dist[i][j]=min(nx.shortest_path_length(G,source=endpoint1,target=j+1, weight="weight") + half_edge_weight,\
			nx.shortest_path_length(G,source=endpoint2,target=j+1, weight="weight") + half_edge_weight)
	return dist


driversNo=5
ODmatrix=create_ODmatrix(driversNo)
print(ODmatrix)


# print(nx.get_node_attributes(G,'pos'))
# E=nx.get_edge_attributes(G,'weight')