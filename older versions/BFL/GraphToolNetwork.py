import graph_tool.all as gt

class GraphToolNetwork:
	def __init__(self):
		self.Ggt = gt.Graph(directed = False)
		self.nxToGtNodesDict = {}
		self.nxToGtEdgesDict = {}
		self.gtEdgeWeights = self.Ggt.new_edge_property("double")


	def createGraphToolNetworkFromGnx(self, Gnx):
		nxNodes = Gnx.nodes()
		nxEdges = list(Gnx.edges())

		for nxNode in nxNodes:
			gtNodeId = self.Ggt.add_vertex()
			self.nxToGtNodesDict[nxNode] = gtNodeId
		for nxEdgeSource, nxEdgeTarget in nxEdges:
			gtEdgeSource = self.nxToGtNodesDict[nxEdgeSource]
			gtEdgeTarget = self.nxToGtNodesDict[nxEdgeTarget]
			gtEdgeId = self.Ggt.add_edge(gtEdgeSource, gtEdgeTarget)
			self.nxToGtEdgesDict[(nxEdgeSource, nxEdgeTarget)] = gtEdgeId
			self.gtEdgeWeights[gtEdgeId] = Gnx[nxEdgeSource][nxEdgeTarget]["weight"]