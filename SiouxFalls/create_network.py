import matplotlib.pyplot as plt
import networkx as nx
import math


def create_network(plot=False):
	nodes_file='TransportationNetworks/SiouxFalls/SiouxFalls_node.tntp'
	fp1=open(nodes_file,"r")
	xcoords=[]
	ycoords=[]
	G=nx.Graph()
	i=1
	next(fp1)
	for line in fp1:
		elements=line.split("\t")
		x=float(elements[1])
		y=float(elements[2])
		# xcoords.append(x/10000)
		# ycoords.append(y/10000)
		G.add_node(i,pos=(x/10000, y/10000))
		i=i+1
	fp1.close()

	net_file='TransportationNetworks/SiouxFalls/SiouxFalls_net.tntp'
	fp2=open(net_file,"r")
	origin_nodes=[]
	dest_nodes=[]
	weights=[]
	for i in range(8):
		next(fp2)
	for line in fp2:
		elements=line.split("\t")
		origin=int(elements[1])
		dest=int(elements[2])
		capacity=math.ceil(float(elements[3]))
		# origin_nodes.append(origin)
		# dest_nodes.append(dest)
		weights.append(capacity)
		G.add_edge(origin,dest,weight=capacity)
	fp2.close()
	if plot:
		pos=nx.get_node_attributes(G,'pos')
		# labels = nx.get_edge_attributes(G,'weight')
		nx.draw(G, pos, with_labels = True)
		# labels=nx.draw_networkx_labels(G,pos=nx.spring_layout(G))
		# nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
		plt.show()
	return G, weights


# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(xcoords, ycoords, color='darkgreen', marker='o')
# plt.show()