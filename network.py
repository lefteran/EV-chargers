import matplotlib.pyplot as plt
import networkx as nx
import math
import json



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