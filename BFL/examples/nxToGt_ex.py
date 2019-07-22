import networkx as nx
import graph_tool.all as gt

########################## Gnx ###################################
Gnx = nx.Graph()
for i in range(6):
    nodeId = '7845695' + str(i)
    lat, lon = -87.8314656000,41.9846967000
    Gnx.add_node(nodeId, pos = (lat, lon))
nxNodes = Gnx.nodes()
print("nxNodes are", nxNodes)

Gnx.add_edge("78456950","78456952", weight=7)
Gnx.add_edge("78456951","78456953", weight=2)
Gnx.add_edge("78456951","78456954", weight=3)
Gnx.add_edge("78456952","78456953", weight=4)
Gnx.add_edge("78456952","78456954", weight=15)

a=Gnx["78456952"]["78456954"]["weight"]
# print("a is ", a)

nxEdges = list(Gnx.edges())
print("nxEdges are ", nxEdges)

startNode = "78456950"
facilityKey = "78456955"
# nxDist = nx.shortest_path_length(Gnx, source=startNode, target=facilityKey, weight='weight')
# print("nxDist is ", nxDist)

########################## Ggt ###################################
nxToGtNodesDict = {}                            #Alternatively use  new_vertex_property() for the node ids
Ggt = gt.Graph(directed=False)
for nxNode in nxNodes:
    gtNodeId = Ggt.add_vertex()
    nxToGtNodesDict[nxNode] = gtNodeId
    # print("v is ", gtNodeId)

gtEdgeWeights = Ggt.new_edge_property("double")
for nxEdgeSource, nxEdgeTarget in nxEdges:
    # print("edge source is %s and target is %s" %(nxEdgeSource, nxEdgeTarget))
    gtEdgeSource = nxToGtNodesDict[nxEdgeSource]
    gtEdgeTarget = nxToGtNodesDict[nxEdgeTarget]
    gtEdgeId = Ggt.add_edge(gtEdgeSource, gtEdgeTarget)
    gtEdgeWeights[gtEdgeId] = Gnx[nxEdgeSource][nxEdgeTarget]["weight"]

gtDist = gt.shortest_distance(Ggt, source = nxToGtNodesDict[startNode], target=nxToGtNodesDict[facilityKey], weights=gtEdgeWeights)
print("gtDist is ", gtDist)

# for v in Ggt.vertices():
#     print("v is ", v)
# for e in Ggt.edges():
#     print("e is ", e)
#     print("weight of e is ", gtEdgeWeights[e])