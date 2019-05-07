from shapely import geometry
import json
import itertools
import time
import network as nrk


def getNetworkBoundariesDict():
	with open('Chicago/ChicagoZoning.geojson') as fz:
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


def findAdjacencies(boundariesDict):
	count = 0
	adjacencyDict = {}
	combinations = [[key for key in dictItem] for dictItem in itertools.combinations(boundariesDict, 2)]
	for combination in combinations:
		id1 = combination[0]
		id2 = combination[1]
		if id1 not in adjacencyDict:
			adjacencyDict[id1] = []
		if id2 not in adjacencyDict:
			adjacencyDict[id2] = []
		polygon1 = boundariesDict[id1]
		polygon2 = boundariesDict[id2]
		if polygon1.touches(polygon2):
			adjacencyDict[id1].append(id2)
			adjacencyDict[id2].append(id1)
			count +=1
	for key, adjList in adjacencyDict.items():
		adjacencyDict[key].append(key)
	print("there are %d adjacencies" %count)
	return adjacencyDict


def exportAdjacencyDict(adjacencyDict):
	boundaryAdjacencies = "boundaryAdjacencies.txt"
	fp = open(boundaryAdjacencies,"w")
	for key, adjList in adjacencyDict.items():
		fp.write("%s" %key)
		for item in adjList:
			fp.write(", %s" %item)
		fp.write("\n")
	fp.close()


def polyContainsPoint(polygon, point):
	return polygon.contains(point)


def getBelongingDict(boundariesDict, G):
	belongingDict = {}
	count = 0
	for boundaryKey, polygon in boundariesDict.items():
		count += 1
		if boundaryKey not in belongingDict:
			belongingDict[boundaryKey] = []
		for nodeId, data in G.nodes(data=True):
			lat = G.nodes[nodeId]['pos'][0]
			lon = G.nodes[nodeId]['pos'][1]
			point = geometry.Point(lat,lon)
			if polyContainsPoint(polygon, point):
				belongingDict[boundaryKey].append(nodeId)
		# print("lat is %f and lon is %f" %(lat,lon))
		print("boundary No: ", count)
	return belongingDict


def exportBelonging(belongingDict):
	belonging = "belonging.txt"
	fp = open(belonging,"w")
	for key, belongingList in belongingDict.items():
		fp.write("%s" %key)
		for item in belongingList:
			fp.write(", %s" %item)
		fp.write("\n")
	fp.close()

def polygonContainsPolygon(polygon1, polygon2):
	return False


# def createZones():
# 	zone = zn.Zone(boundaryId, adjacent, demand, zoneFacilities, onStreetBound)

start_time = time.time()
G = nrk.getNetworkNodes()
boundariesDict = getNetworkBoundariesDict()
belongingDict = getBelongingDict(boundariesDict, G)
exportBelonging(belongingDict)
# adjacencyDict = findAdjacencies(boundariesDict)
# exportAdjacencyDict(adjacencyDict)

print("--- %s seconds ---" % (time.time() - start_time))











	# for polygon1,polygon2 in itertools.combinations(polygons, 2):
	# 	if polygon1.touches(polygon2):
	# 		print("there are adjacencies")