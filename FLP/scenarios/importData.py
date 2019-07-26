import matplotlib.pyplot as plt
import networkx as nx
import _pickle as pickle
import facility as fl
import zone as zn
import vehicle as vh
import json
import tripTimes
import serializationIO
import settings


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

def importNetwork():
	Gnx = importNodes('Chicago/ChicagoNodes.geojson')
	importEdges(Gnx, 'Chicago/ChicagoEdges.geojson')
	belongingDict, nonBelongingNodeIds = importBelongingDict('Chicago/nodeInBoundary.csv')
	invBelongingDict = importInvBelonging('Chicago/BoundaryNodes.csv')
	Gnx.remove_nodes_from(nonBelongingNodeIds)
	adjacencyDict = importAdjacencyDict('Chicago/adjacencies.csv')

	facilityDataDict = importFacilityData('Chicago/FacilityData.csv')
	facilitiesDict = {}
	for facilityId, facilityList in facilityDataDict.items():
		if facilityId in belongingDict:
			facilitiesDict[facilityId] = fl.Facility(facilityId, float(facilityList[0]), int(facilityList[1]),\
			int(facilityList[2]), belongingDict[facilityId][0])

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

	settings.parameters.adjacencyDict = adjacencyDict
	settings.parameters.belongingDict = belongingDict
	settings.parameters.facilitiesDict = facilitiesDict
	settings.parameters.zonesDict = zonesDict

	return Gnx


def importParameters(filename):
	with open(filename, 'rb') as parametersInput:
		return pickle.load(parametersInput)


def getVehicles(Gnx):
	if settings.flags.importVehiclesDict:
		vehiclesDict = serializationIO.importAndDeserialize('Chicago/vehiclesDict.json')
	else:	# INSTEAD OF IMPORTING DATA FROM THE FILE VehicleData.csv BELOW, GENERATE RANDOM INSTANCES
		# TODO: Create a method to randomly generate the locations of the vehicles instead of reading them from a file
		vehicleDataDict = importVehicleData('Chicago/VehicleData.csv')
		vehiclesDict = {}
		for vehicleId, vehicleDataList in vehicleDataDict.items():
			startNode = vehicleDataList[0]
			endNode = vehicleDataList[1]
			if Gnx.has_edge(startNode, endNode):
				vehiclesDict[vehicleId] = vh.Vehicle(vehicleId, startNode, endNode, float(vehicleDataList[2]))
	# serialization.serializeAndExport(parameters.vehiclesDict, 'Chicago/vehiclesDict.json')
	settings.parameters.vehiclesDict = vehiclesDict

def getTimes(Gnx, GtNetwork):
	if settings.flags.importTimes:
		timesDict = importDeterministicTripTimes('Chicago/vehicleFacilityTimes.csv')
	else:
		if not settings.flags.useGraphTool:
			timesDict = tripTimes.getTimeDictNx(Gnx)
		else:
			if settings.flags.parallelComputationOfTimes:
				timesDict = tripTimes.getTimeDictGtParallel(GtNetwork)
			else:
				timesDict = tripTimes.getTimeDictGt(GtNetwork)
	settings.parameters.timesDict = timesDict

