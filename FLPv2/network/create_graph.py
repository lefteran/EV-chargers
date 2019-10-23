# LIBRARIES
import json
import networkx as nx
# FILES
import settings


def read_json_file(filename):
	with open(filename) as json_file:
		json_dict = json.load(json_file)
	return json_dict

def create_graph():
	json_dict = read_json_file(settings.chicago_json_network)
	graph = nx.Graph()
	for node in json_dict['nodes']:
		graph.add_node(node['id'])
		graph.nodes[node['id']]['id'] = node['id']
		graph.nodes[node['id']]['y'] = node['y']
		graph.nodes[node['id']]['x'] = node['x']

	for edge in json_dict['links']:
		graph.add_edge(edge['source'], edge['target'])
		graph.edges[edge['source'], edge['target']]['id'] = edge['osmid']
		graph.edges[edge['source'], edge['target']]['length'] = edge['length']
		graph.edges[edge['source'], edge['target']]['traveltime'] = edge['traveltime']
		if 'geometry' in edge:
			graph.edges[edge['source'], edge['target']]['geometry'] = edge['geometry']
	return graph





