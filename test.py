# from shapely import geometry
# from matplotlib import pyplot as plt
# from random import choice
# import itertools
# import networkx as nx
# import json

# point1 = geometry.Point(0.5, 0.5)

# # mypoints = [[-87.71024494329944,41.87679179024591],[-87.71017533609232,41.87680982098899],[-87.71007717906045,41.876837032688094],[-87.70995840840602,41.87686940137096],[-87.70986776753541,41.876893936607445],[-87.70979892451263,41.87691227890078],[-87.70974032377826,41.876927081527725],[-87.70965984049518,41.876947750497],[-87.70965637988034,41.87694864004993],[-87.7096571731452,41.8769417154028],[-87.70965722690596,41.87694124670255],[-87.70965430150487,41.87694128323064],[-87.70956796248369,41.87694236399029],[-87.70956750328092,41.876921844390445],[-87.70956732460937,41.87691386149636],[-87.7095670409318,41.87690119524487],[-87.7095655140866,41.87683164767299],[-87.70956406067798,41.87676210049915],[-87.7095625338375,41.87669255292559],[-87.70956100699941,41.87662300535121],[-87.70955955359766,41.876553458174854],[-87.70955802729796,41.876483855716685],[-87.70955650046699,41.876414308139786],[-87.70955504707209,41.87634476096092],[-87.70955352024583,41.876275213382335],[-87.70964659303334,41.87627404900402],[-87.70973706287742,41.876272917068505],[-87.7102080753441,41.87626696653279],[-87.71023479959487,41.87626662827075],[-87.71023377297385,41.87629021254529],[-87.71023434870388,41.87633678558577],[-87.71023561578566,41.876406688498705],[-87.71023706332618,41.876458013820205],[-87.71023925686231,41.876542164413465],[-87.71024034116542,41.876611984004725],[-87.71024176158838,41.876677442062075],[-87.71024494329944,41.87679179024591]]

# # reorder = [1,0]
# # mypoints = []
# polygon1 = [[0,0], [0,1], [1,1], [1,0]]
# polygon2 = [[0.75,0.8], [0.75,0.2], [2,0.2], [2,0.8]]
# # for point in mypointsOrig:
# #         newpoint = [point[i] for i in reorder]
# #         mypoints.append(newpoint)
# # print(mypoints)

# pointList = []
# for point in polygon1:
#         p = geometry.Point(point)
#         pointList.append(p)
# poly1 = geometry.Polygon([(p.x, p.y) for p in pointList])
# x1,y1 = poly1.exterior.xy

# pointList = []
# for point in polygon2:
#         p = geometry.Point(point)
#         pointList.append(p)
# poly2 = geometry.Polygon([(p.x, p.y) for p in pointList])
# x2,y2 = poly2.exterior.xy

# # if poly1.touches(poly2):
# #         print("there are adjacencies")

# # fig = plt.figure(1, figsize=(5,5), dpi=90)
# # ax = fig.add_subplot(111)
# # ax.plot(x1, y1, color='#6699cc', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
# # ax.plot(x2, y2, color='green', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
# # # plt.scatter(point1.x, point1.y, s=10, c='red')
# # ax.set_title('Polygon')
# # plt.show()


# # polygons = [geometry.Polygon([(0,0),(0,1),(1,1),(1,0)]), geometry.Polygon([(1,0),(1,1),(2,1),(2,0)]), geometry.Polygon([(2,1),(2,2),(3,2),(3,1)])]
# # print(polygons[0].touches(polygons[1]))



# # d = {'x': 1, 'y': 2, 'z': 3} 
# # for key, value in d.items():
# #     print("key is ", key)
# #     print("value is ", value)


# options = {
#     "x": ["a", "b"],
#     "y": [10, 20, 30],}


# # keys = options.keys()
# # values = (options[key] for key in keys)
# # combinations = [dict(zip(keys, combination)) for combination in itertools.product(*values)]
# # print(combinations)

# combination_dict = {"one": [1, 2, 3], "two": [2, 3, 4], "three": [3, 4, 5]}

# # results = [[j for j in i] for i in itertools.combinations(combination_dict, 2)]
# # for item in results:
# #         print(combination_dict[item[1]])
# # for item1, item2 in result_list:
# #         print(item2)

# # adjDict = {}
# # adjDict[545] = []
# # adjDict[545].append(14)
# # adjDict[9461] = [64565,487]
# # for key, adjList in adjDict.items():
# #         print("%s" %key, end='', flush=True)
# #         for item in adjList:
# #                 print(", %s" %item, end='', flush=True)
# #         print("\n")

# # for i in range(len(adjDict)):
# #         print(i)
# # print(adjDict[545])



# # G = nx.Graph()
# # with open('Chicago/ChicagoNodes.geojson') as fn:
# #         data = json.load(fn)
# # for feature in data['features']:
# #         nodeId = feature['properties']['identifier']
# #         coordinates = feature['geometry']['coordinates']
# #         lat = coordinates[1]
# #         lon = coordinates[0]
# #         G.add_node(nodeId, pos = (lat, lon))

# # for node, data in G.nodes(data=True):
# #         lat = G.nodes[node]['pos'][0]
# #         lon = G.nodes[node]['pos'][1]
# #         point = geometry.Point(lat,lon)
        

# # def getNetworkBoundariesDict():
# # 	with open('Chicago/ChicagoZoning.geojson') as fz:
# # 		data = json.load(fz)
# # 	boundariesDict = {}
# # 	count = 0
# # 	for feature in data['features']:
# # 		pointList = []
# # 		boundaryId = feature['properties']['zoning_id']
# # 		coordinates = feature['geometry']['coordinates']
# # 		boundaryPoints = coordinates[0][0]
# # 		for point in boundaryPoints:
# # 			p = geometry.Point(point)
# # 			pointList.append(p)
# # 		polygon = geometry.Polygon([[p.x, p.y] for p in pointList])
# # 		boundariesDict[boundaryId] = polygon
# # 		count += 1
# # 	print("There are %d polygons" %count)
# # 	return boundariesDict


# # boundariesDict = getNetworkBoundariesDict()
# # polygon1 = boundariesDict["9428"]
# # polygon2 = boundariesDict["15481"]
# # a= polygon1.contains(polygon2)
# # b= polygon2.contains(polygon1)
# # print("a is ", a)
# # print("b is ", b)


 

# G = nx.Graph()

# G.add_edge("1","2", weight=7)
# G.add_edge("1","3", weight=2)
# G.add_edge("1","4", weight=3)
# G.add_edge("2","3", weight=4)
# G.add_edge("2","4", weight=15)


# a=nx.shortest_path_length(G, source="1", target="2", weight='weight')
# # print("a is %f" %a)
# edges = list(G.edges())
# # print(G.nodes())
# edgeId = choice(edges)

# # (u,v) = edgeId
# # print("u is ", u)
# # G.remove_nodes_from([1])
# # print(G.nodes())
# # print(G.edges())

# import operator
# import _pickle as pickle
# import ujson

# class Student:
#     def __init__(self, name, grade, age):
#         self.name = name
#         self.grade = grade
#         self.age = age


# studi1=Student('john', 'A', 15)
# studi2=Student('dave', 'B', 10)
# studi3=Student('jane', 'B', 12)

# student_Dict = {}
# student_Dict[studi1.name]=studi1
# student_Dict[studi2.name]=studi2
# student_Dict[studi3.name]=studi3

# L = sorted(student_Dict.values(), key=operator.attrgetter('age'), reverse=True)
# L.sort(key=operator.attrgetter('age'), reverse=False)
# for student in L:
#     print(student.name)


# import itertools


# L=[1,2,3]
# for i in range(2):
#     M=list(itertools.combinations(L, i+1))
#     print(M)


# g = pickle.loads(pickle.dumps(studi3, -1))
# e = ujson.loads(ujson.dumps(studi3))
# a=2


# vehicle=2
# facility=3
# L=[]
# L.append((2,3))
# print(L[0][1])
#
# newdict = {1:0, 2:0, 3:0}
# print(list(newdict.keys()))

# a=2
# print(f"a is {a}")
#
# from math import floor
#
# a = [1,6,9,8,7,5,6,3,4,6,56,54,57]
# aLength = len(a)
# k=3
# items = floor(aLength / 3)
# print(a[0:4])

import itertools

def getCombinationsOfExactSwaps(listOfItems, numberOfSwaps):
	combs = []
	for subset in itertools.combinations(listOfItems, numberOfSwaps):
		combs.append(list(subset))
	return combs


a=getCombinationsOfExactSwaps([1,2,3,4], 1)
print(a)