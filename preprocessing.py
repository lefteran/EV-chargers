from shapely import geometry
import json
import itertools
import time
import importData as impdt
import sys


def polyContainsPoint(polygon, point):
	return polygon.contains(point)

def getNetworkBoundariesDict(filename):
	with open(filename) as fz:
		data = json.load(fz)
	boundariesDict = {}
	count = 0
	for feature in data['features']:
		pointList = []
		boundaryId = feature['properties']['zoning_id']
		coordinates = feature['geometry']['coordinates']
		boundaryPoints = coordinates[0][0]
		for point in boundaryPoints:
			p = geometry.Point(point)
			pointList.append(p)
		polygon = geometry.Polygon([[p.x, p.y] for p in pointList])
		boundariesDict[boundaryId] = polygon
		count += 1
	print("There are %d polygons" %count)
	return boundariesDict


# ################## BELONGING ############################

def getNodeInBoundaryDict(boundariesDict, G):
	belongingDict = {}
	count = 0
	for nodeId, data in G.nodes(data=True):
		count += 1
		lat = G.nodes[nodeId]['pos'][0]
		lon = G.nodes[nodeId]['pos'][1]
		point = geometry.Point(lat,lon)
		if nodeId not in belongingDict:
			belongingDict[nodeId] = []
		for boundaryKey, polygon in boundariesDict.items():
			if polyContainsPoint(polygon, point):
				belongingDict[nodeId].append(boundaryKey)
		print("Point No (belonging): ", count)
	return belongingDict


def ensureNodeBelongsToOneBounary(belongingDict, boundariesDict):
	newBelongingDict = {}
	for nodeId, boundariesList in belongingDict.items():
		if len(boundariesList) > 1:
			id1 = boundariesList[0]
			id2 = boundariesList[1]
			polygon1 = boundariesDict[id1]
			polygon2 = boundariesDict[id2]
			if polygon1.contains(polygon2):
				newBelongingDict[nodeId] = [id2]
			else:
				newBelongingDict[nodeId] = [id1]
		else:
			newBelongingDict[nodeId] = belongingDict[nodeId]
	return newBelongingDict


def exportBelonging(belongingDict, filename):
	fp = open(filename,"w")
	for key, belongingList in belongingDict.items():
		fp.write("%s" %key)
		for item in belongingList:
			fp.write(", %s" %item)
		fp.write("\n")
	fp.close()

# #################### ADJACENCY #################################

def getAdjacenciesDict(boundariesDict):
	countAdjacencies = 0
	adjacencyDict = {}
	combinations = [[key for key in dictItem] for dictItem in itertools.combinations(boundariesDict, 2)]
	totalCombinations = len(combinations)
	combinationCount = 0
	for combination in combinations:
		combinationCount += 1
		print("Checking adjacency %d of %d" %(combinationCount, totalCombinations))
		id1 = combination[0]
		id2 = combination[1]
		if id1 not in adjacencyDict:
			adjacencyDict[id1] = []
		if id2 not in adjacencyDict:
			adjacencyDict[id2] = []
		polygon1 = boundariesDict[id1]
		polygon2 = boundariesDict[id2]
		if polygon1.touches(polygon2) or polygon1.contains(polygon2) or polygon2.contains(polygon1):
			adjacencyDict[id1].append(id2)
			adjacencyDict[id2].append(id1)
			countAdjacencies +=1
	for key, adjList in adjacencyDict.items():
		adjacencyDict[key].append(key)
	print("there are %d adjacencies" %countAdjacencies)
	return adjacencyDict


def exportAdjacencyDict(adjacencyDict, filename):
	fp = open(filename,"w")
	for key, adjList in adjacencyDict.items():
		fp.write("%s" %key)
		for item in adjList:
			fp.write(", %s" %item)
		fp.write("\n")
	fp.close()



def preprocessing(doPreprocessing):
	if doPreprocessing:
		start_time = time.time()

		G = impdt.importNodes('Chicago/ChicagoNodes.geojson')
		boundariesDict = getNetworkBoundariesDict('Chicago/ChicagoZoning.geojson')

		nodeInBoundaryDict = getNodeInBoundaryDict(boundariesDict, G)
		belongingDict = ensureNodeBelongsToOneBounary(nodeInBoundaryDict, boundariesDict)
		exportBelonging(belongingDict, "Chicago/belongingNode_Boundary.csv")
		
		adjacencyDict = getAdjacenciesDict(boundariesDict)
		exportAdjacencyDict(adjacencyDict, "Chicago/adjacencies.csv")
		
		print("--- Preprocessing: %s seconds ---" % (time.time() - start_time))
