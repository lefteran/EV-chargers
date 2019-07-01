import networkx as nx
import matplotlib.pyplot as plt

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




# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(xcoords, ycoords, color='darkgreen', marker='o')
# plt.show()