# LIBRARIES
import matplotlib.cm as cm
import matplotlib.colors as colors
import networkx as nx
import json
import osmnx as ox
import network.nx_graph as nx_graph
import pandas as pd
# FILES
import settings
import network.recharging_nodes as vehicles_per_hour


def plotGraph(graph):
	fig, ax = ox.plot_graph(graph, bgcolor='k', node_size=3, node_color='#999999', node_edgecolor='none', node_zorder=2,
                            edge_color='#555555', edge_linewidth=0.5, edge_alpha=1)

def visualise_nodes(graph, place, vehicles_locations_list, facility_locations):
	nc = list()
	ns = list()
	for node, data in graph.nodes(data=True):
		if node in vehicles_locations_list:
			nc.append('#F1E443')
			ns.append(10)
			# solutionCoordinates.append((G.nodes[node]['lat'], G.nodes[node]['lon']))
		elif str(node) in facility_locations:
			if str(node) == '1764470748':
				nc.append('r')
				ns.append(15)
			else:
				nc.append('b')
				ns.append(2.5)
			# candidatesCoordinates.append((G.nodes[node]['lat'], G.nodes[node]['lon']))
		else:
			# nc.append('b')
			# nc.append('#00ffff')
			nc.append('None')
			# ns.append(0.7)
			ns.append(0)

	fig, ax = ox.plot_graph(graph, bgcolor='#CFCCCB', node_size=ns, node_color=nc, node_edgecolor='none', node_zorder=2,
                            edge_color='#555555', edge_linewidth=0.3, edge_alpha=1, dpi=500)
	# fig.savefig('figures/' + place + 'qiming.png', #facecolor=fig.get_facecolor(), dpi=300)



def load_graphml_network():
	return ox.load_graphml(settings.chicago_graphml_network)


def get_list_of_all_vehicles_locations_over_day():
	settings.vehicles_network_locations_per_hour_dict = vehicles_per_hour.load_recharging_nodes_per_hour_dict()
	vehicles_locations = list()
	for _, vehicles_per_hour_list in settings.vehicles_network_locations_per_hour_dict.items():
		vehicles_locations.extend(vehicles_per_hour_list)
	return list(set(vehicles_locations))

def load_solution_dict():
	filename = settings.solution_path
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict


def visualise_network(place):
	ox.config(log_console=True, use_cache=True)

	vehicles_locations_list = get_list_of_all_vehicles_locations_over_day()
	solution_dict = load_solution_dict()
	facility_locations = solution_dict['solution_list']

	graph = load_graphml_network()
	# graph = nx_graph.create_graph()

	visualise_nodes(graph, place, vehicles_locations_list, facility_locations)













