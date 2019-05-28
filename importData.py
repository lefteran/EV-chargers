import matplotlib.pyplot as plt
from shapely import geometry
import networkx as nx
# import math
import facility as fl
import zone as zn
import vehicle as vh
import json
import dataClass
# import itertools


def importNodes(filename):
	G = nx.Graph()
	with open(filename) as fn:
		data = json.load(fn)
	for feature in data['features']:
		nodeId = feature['properties']['identifier']
		coordinates = feature['geometry']['coordinates']
		lat = coordinates[0]
		lon = coordinates[1]
		G.add_node(nodeId, pos = (lat, lon))
	return G


def importEdges(G, filename):
	with open(filename) as fe:
		data = json.load(fe)
	for feature in data['features']:
		startNode = feature['properties']['startNode']
		endNode = feature['properties']['endNode']
		length = float(feature['properties']['length'])
		G.add_edge(startNode, endNode, weight = length)


def importBelongingDict(filename):
	belongingDict = {}
	nonBelongingNodeIds = []
	fp = open(filename,"r")
	for line in fp:
		elements = line.split(",")
		key = elements[0].strip()
		if len(elements) < 2:
			nonBelongingNodeIds.append(key)
		else:
			belongingDict[key] = []
			for i in range(len(elements) - 1):
				belongingDict[key].append(elements[i+1].strip())
	fp.close()
	return belongingDict, nonBelongingNodeIds


def importInvBelonging(filename):
	invBelongingDict = {}
	fp = open(filename,"r")
	for line in fp:
		elements = line.split(",")
		key = elements[0].strip()
		invBelongingDict[key] = []
		for i in range(len(elements) - 1):
			invBelongingDict[key].append(elements[i+1].strip())
	fp.close()
	return invBelongingDict


def importAdjacencyDict(filename):
	adjacencyDict = {}
	fp = open(filename,"r")
	for line in fp:
		elements = line.split(",")
		key = elements[0].strip()
		adjacencyDict[key] = []
		for i in range(len(elements) - 1):
			adjacencyDict[key].append(elements[i+1].strip())
	fp.close()
	return adjacencyDict

def importFacilityData(filename):
	facilityDataDict = {}
	fp = open(filename,"r")
	for line in fp:
		elements = line.split(",")
		key = elements[0].strip()
		facilityDataDict[key] = []
		for i in range(len(elements) - 1):
			facilityDataDict[key].append(elements[i+1].strip())
	fp.close()
	return facilityDataDict

def importZoneData(filename):
	zoneDataDict = {}
	fp = open(filename,"r")
	for line in fp:
		elements = line.split(",")
		key = elements[0].strip()
		if key == '621':
			a=2
		zoneDataDict[key] = []
		for i in range(len(elements) - 1):
			zoneDataDict[key].append(elements[i+1].strip())
	fp.close()
	return zoneDataDict

def importVehicleData(filename):
	vehicleDataDict = {}
	fp = open(filename,"r")
	for line in fp:
		elements = line.split(",")
		key = elements[0].strip()
		vehicleDataDict[key] = []
		for i in range(len(elements) - 1):
			vehicleDataDict[key].append(elements[i+1].strip())
	fp.close()
	return vehicleDataDict

def importDeterministicTripTimes(filename):
	timesDict = {}
	vehicleTimesDict = {}
	fp = open(filename,"r")
	vehicleKey = 0
	for line in fp:
		elements = line.split(",")
		key = elements[0].strip()
		facilityKey = elements[1].strip()
		tripTime = float(elements[2].strip())
		if key != vehicleKey and vehicleKey != 0:
			timesDict[vehicleKey] = vehicleTimesDict
			vehicleTimesDict = {}
			vehicleKey = key
		vehicleTimesDict[facilityKey] = tripTime
		vehicleKey = key
	timesDict[vehicleKey] = vehicleTimesDict
	fp.close()
	return timesDict


def cleanZoneIds(adjacencyDict, IdsList):
	for IdToRemove in IdsList:
		if IdToRemove in adjacencyDict:
			for neighboringZoneId in adjacencyDict[IdToRemove]:
				adjacencyDict[neighboringZoneId].remove(IdToRemove)
	# zoneId='621' was not found in zoneDict because it is not in invBelongingDict
	# (check the next method). 
	# if zoneId not in invBelongingDict remove it from the adjacencyDict
	# i.e. for any neighbZoneId in zoneDict[zoneId].adjacent
	# 			zoneDict[neighbZoneId].adjacent.remove(zoneId)


def importNetworkAndDicts():
	G = importNodes('Chicago/ChicagoNodes.geojson')
	importEdges(G, 'Chicago/ChicagoEdges.geojson')
	belongingDict, nonBelongingNodeIds = importBelongingDict('Chicago/nodeInBoundary.csv')
	invBelongingDict = importInvBelonging('Chicago/BoundaryNodes.csv')
	G.remove_nodes_from(nonBelongingNodeIds)
	adjacencyDict = importAdjacencyDict('Chicago/adjacencies.csv')

	facilityDataDict = importFacilityData('Chicago/FacilityData.csv')
	facilitiesDict = {}
	for facilityId, facilityList in facilityDataDict.items():
		if facilityId in belongingDict:
			facilitiesDict[facilityId] = fl.Facility(facilityId, float(facilityList[0]), int(facilityList[1]),\
			int(facilityList[2]), belongingDict[facilityId])

	zoneDataDict = importZoneData('Chicago/ZoneData.csv')
	zonesDict = {}
	nonBelongingZoneDictIds = []
	for zoneId, zoneDataList in zoneDataDict.items():
		if zoneId in invBelongingDict:
			zonesDict[zoneId] = zn.Zone(zoneId, adjacencyDict[zoneId], int(zoneDataList[0]), invBelongingDict[zoneId],\
			int(zoneDataList[1]))
		else:
			nonBelongingZoneDictIds.append(zoneId)
	cleanZoneIds(adjacencyDict, nonBelongingZoneDictIds)

	vehicleDataDict = importVehicleData('Chicago/VehicleData.csv')
	vehiclesDict = {}
	for vehicleId, vehicleDataList in vehicleDataDict.items():
		startNode = vehicleDataList[0]
		endNode = vehicleDataList[1]
		if G.has_edge(startNode, endNode):
			vehiclesDict[vehicleId] = vh.Vehicle(vehicleId, startNode, endNode, float(vehicleDataList[2]))
	timesDict = importDeterministicTripTimes('Chicago/vehicleFacilityTimes.csv')
	# timesDict = trtim.getTimeDict(G, facilitiesDict, vehiclesDict)
	# trtim.exportDeterministicTripTimes(timesDict, 'Chicago/vehicleFacilityTimes.csv')

	parameters = dataClass.dataClass()
	parameters.adjacencyDict = adjacencyDict
	parameters.belongingDict = belongingDict
	parameters.facilitiesDict = facilitiesDict
	parameters.zonesDict = zonesDict
	parameters.vehiclesDict = vehiclesDict
	parameters.timesDict = timesDict

	return parameters







# # ####################### Sioux Falls ###################################

# def createNetwork():
# 	G = nx.Graph()
# 	with open('SiouxFalls/SiouxFallsCoordinates.geojson') as fp:
# 		data = json.load(fp)
# 	for feature in data['features']:
# 		nodeId = feature['properties']['id']
# 		coordinates = feature['geometry']['coordinates']
# 		lat = coordinates[1]
# 		lon = coordinates[0]
# 		G.add_node(nodeId, pos = (lat, lon))

# 	net_file = 'SiouxFalls/SiouxFalls_net.tntp'
# 	fpe = open(net_file,"r")
# 	weights = []
# 	for i in range(8):
# 		next(fpe)
# 	for line in fpe:
# 		elements = line.split("\t")
# 		origin = int(elements[1])
# 		dest = int(elements[2])
# 		capacity = round(float(elements[3]) / 100, 2)
# 		weights.append(capacity)
# 		G.add_edge(origin, dest, weight = capacity)
# 	fpe.close()
# 	return G, weights




# def polyContainsPoint(polygon, point):
# 	return polygon.contains(point)


# G = getNetworkNodes()
# getNetworkEdges(G)




# G, weights = createNetwork()
# edges = G.edges()
# print(edges)
# print(G[1][2]['weight'])
# path = nx.dijkstra_path(G, source=1, target=4, weight='weight')
# print(path)
# dist = nx.shortest_path_length(G, source=1, target=4, weight='weight')
# print(dist)
# plotNetwork(G)







