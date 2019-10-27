import networkx as nx
import graph_tool.all as gt
import json

class GraphToolNetwork:
	def __init__(self):
		self.graph_gt = gt.Graph(directed = False)
		self.nx_to_gt_nodes_dict = {}
		self.nx_to_gt_edges_dict = {}
		self.gt_edge_lengths = self.graph_gt.new_edge_property("double")
		self.gt_edge_travel_times = self.graph_gt.new_edge_property("double")


	def create_graph_tool_network_from_gnx(self, graph_nx):
		nx_nodes = graph_nx.nodes()
		nx_edges = list(graph_nx.edges())

		for nxNode in nx_nodes:
			gt_node_id = self.graph_gt.add_vertex()
			self.nx_to_gt_nodes_dict[nxNode] = gt_node_id
		for nxEdgeSource, nxEdgeTarget in nx_edges:
			gt_edge_source = self.nx_to_gt_nodes_dict[nxEdgeSource]
			gt_edge_target = self.nx_to_gt_nodes_dict[nxEdgeTarget]
			gt_edge_id = self.graph_gt.add_edge(gt_edge_source, gt_edge_target)
			self.nx_to_gt_edges_dict[(nxEdgeSource, nxEdgeTarget)] = gt_edge_id
			self.gt_edge_lengths[gt_edge_id] = graph_nx[nxEdgeSource][nxEdgeTarget]["length"]
			self.gt_edge_travel_times[gt_edge_id] = graph_nx[nxEdgeSource][nxEdgeTarget]["traveltime"]


	def get_vehicles_distances_to_candidates_dict(self, candidate_nodes, vehicles_nodes):
		vehicles_distances_to_candidates_dict = dict()
		for source_node in vehicles_nodes:
			for target_node in candidate_nodes:
				distance = gt.shortest_distance(self.graph_gt, source=self.nx_to_gt_nodes_dict[source_node],
												target=self.nx_to_gt_nodes_dict[int(target_node)], weights=self.gt_edge_lengths)
				vehicles_distances_to_candidates_dict[str(source_node)+ '-' + str(target_node)] = distance
		return vehicles_distances_to_candidates_dict

	def get_vehicles_travel_times_to_candidates_dict(self, candidate_nodes, vehicles_nodes):
		# from tqdm import tqdm
		vehicles_travel_times_to_candidates_dict = dict()
		for source_node in vehicles_nodes:
			for target_node in candidate_nodes:
				travel_time = gt.shortest_distance(self.graph_gt, source=self.nx_to_gt_nodes_dict[source_node],
												target=self.nx_to_gt_nodes_dict[int(target_node)], weights=self.gt_edge_travel_times)
				vehicles_travel_times_to_candidates_dict[str(source_node)+ '-' + str(target_node)] = travel_time
		return vehicles_travel_times_to_candidates_dict








