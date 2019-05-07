import matplotlib.pyplot as plt
from shapely import geometry
import networkx as nx
import math
import json
import itertools
import fiona


def importNodes(filename):
	G = nx.Graph()
	with open(filename) as fn:
		data = json.load(fn)
	for feature in data['features']:
		nodeId = feature['properties']['identifier']
		coordinates = feature['geometry']['coordinates']
		lat = coordinates[0]
		lon = coordinates[1]
		G.add_node(nodeId, pos = (lat, lon))
	return G


# 'Chicago/ChicagoEdges.geojson'
def importEdges(G, filename):
	with open(filename) as fe:
		data = json.load(fe)
	for feature in data['features']:
		startNode = feature['properties']['startNode']
		endNode = feature['properties']['endNode']
		length = feature['properties']['length']
		G.add_edge(startNode, endNode, weight = length)


# boundaryAdjacencies.csv
def importAdjacencyDict(filename):
	adjacencyDict = {}
	fp = open(filename,"r")
	for line in fp:
		elements = line.split(",")
		key = elements[0].strip()
		adjacencyDict[key] = []
		for i in range(len(elements) - 1):
			adjacencyDict[key].append(elements[i+1].strip())
	fp.close()
	return adjacencyDict

def importBelongingDict(filename):
	belongingDict = {}
	fp = open(filename,"r")
	for line in fp:
		elements = line.split(",")
		key = elements[0].strip()
		belongingDict[key] = []
		for i in range(len(elements) - 1):
			belongingDict[key].append(elements[i+1].strip())
	fp.close()
	return belongingDict


def createNetwork():
	G = nx.Graph()
	with open('SiouxFalls/SiouxFallsCoordinates.geojson') as fp:
		data = json.load(fp)
	for feature in data['features']:
		nodeId = feature['properties']['id']
		coordinates = feature['geometry']['coordinates']
		lat = coordinates[1]
		lon = coordinates[0]
		G.add_node(nodeId, pos = (lat, lon))

	net_file = 'SiouxFalls/SiouxFalls_net.tntp'
	fpe = open(net_file,"r")
	weights = []
	for i in range(8):
		next(fpe)
	for line in fpe:
		elements = line.split("\t")
		origin = int(elements[1])
		dest = int(elements[2])
		capacity = round(float(elements[3]) / 100, 2)
		weights.append(capacity)
		G.add_edge(origin, dest, weight = capacity)
	fpe.close()
	return G, weights


def plotNetwork(G):
	pos = nx.get_node_attributes(G,'pos')
	nx.draw(G, pos)
	labels = nx.get_edge_attributes(G,'weight')
	nx.draw(G, pos, with_labels = True)
	# labels=nx.draw_networkx_labels(G,pos=nx.spring_layout(G))
	nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
	plt.show()


def plotBoundary(poly):			 #, point):
	fig = plt.figure(1, figsize=(5,5), dpi=90)
	ax = fig.add_subplot(111)
	x,y = poly.exterior.xy
	ax.plot(x, y, color='#6699cc', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
	# plt.scatter(point.x, point.y, s=10, c='red')
	ax.set_title('Polygon')
	plt.show()


def polyContainsPoint(polygon, point):
	return polygon.contains(point)


# G = getNetworkNodes()
# getNetworkEdges(G)




# G, weights = createNetwork()
# edges = G.edges()
# print(edges)
# print(G[1][2]['weight'])
# path = nx.dijkstra_path(G, source=1, target=4, weight='weight')
# print(path)
# dist = nx.shortest_path_length(G, source=1, target=4, weight='weight')
# print(dist)
# plotNetwork(G)









# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(xcoords, ycoords, color='darkgreen', marker='o')
# plt.show()