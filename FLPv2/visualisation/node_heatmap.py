# from keys import google_elevation_api_key #replace this with your own API key!
import networkx as nx
import numpy as np
import osmnx as ox


def node_elevation():
	ox.config(log_console=True, use_cache=True)
	version = ox.__version__

	# get the street network for san francisco
	place = 'San Francisco'
	place_query = {'city':'San Francisco', 'state':'California', 'country':'USA'}
	G = ox.graph_from_place(place_query, network_type='drive')


	# add elevation to each of the nodes, using the google elevation API, then calculate edge grades
	# G = ox.add_node_elevations(G, api_key=google_elevation_api_key)
	G = ox.add_edge_grades(G)



	# project the street network to UTM
	G_proj = ox.project_graph(G)



	# get one color for each node, by elevation, then plot the network
	nc = ox.get_node_colors_by_attr(G_proj, 'elevation', cmap='plasma', num_bins=20)
	fig, ax = ox.plot_graph(G_proj, fig_height=6, node_color=nc, node_size=12, node_zorder=2, edge_color='#dddddd')


