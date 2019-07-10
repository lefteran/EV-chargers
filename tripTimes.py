import networkx as nx
import graph_tool.all as gt
from math import floor
from multiprocessing import Process, Manager
from os import getpid, cpu_count


def getTimeDictNx(Gnx, parameters):
    print("Calculating Nx trip times ...")
    timesDict = {}
    beta = [1]
    timeOfDay = 0            # time of a day (24*60 entries) counted in minutes starting from 0:00 and ending in 23:59
    numberOfVehicles = len(parameters.vehiclesDict.items())
    numberOfFacilities = len(parameters.facilitiesDict.items())
    countVeh = 0
    for vehicleKey, vehicleObject in parameters.vehiclesDict.items():
        countVeh += 1
        countFac = 0
        print("Checking vehicle %d out of %d" %(countVeh, numberOfVehicles))
        vehicleTimesDict = {}
        startNode = vehicleObject.startNode
        endNode = vehicleObject.endNode
        edgeWeight = float(Gnx[startNode][endNode]['weight'])
        for facilityKey,_ in parameters.facilitiesDict.items():
            countFac += 1
            print("\tChecking facility %d out of %d" % (countFac, numberOfFacilities))
            # if nx.has_path(G, startNode, facilityKey):
            try:
                time1 = edgeWeight * vehicleObject.pointInEdge + \
                        nx.shortest_path_length(Gnx, source=startNode, target=facilityKey, weight='weight') / beta[timeOfDay]
                time2 = edgeWeight * (1 - vehicleObject.pointInEdge) + \
                        nx.shortest_path_length(Gnx, source=endNode, target=facilityKey, weight='weight') / beta[timeOfDay]
                tripTime = min(time1, time2)
            # else:
            except nx.NetworkXNoPath:
                tripTime = float("inf")
            vehicleTimesDict[facilityKey] = tripTime
        timesDict[vehicleKey] = vehicleTimesDict
    return timesDict


def getTimeDictGt(GtNetwork, parameters):
    print("Calculating Gt trip times ...")
    timesDict = {}
    beta = [1]
    timeOfDay = 0            # time of a day (24*60 entries) counted in minutes starting from 0:00 and ending in 23:59
    numberOfVehicles = len(parameters.vehiclesDict.items())
    numberOfFacilities = len(parameters.facilitiesDict.items())
    countVeh = 0
    for vehicleKey, vehicleObject in parameters.vehiclesDict.items():
        countVeh += 1
        countFac = 0
        print("Checking vehicle %d out of %d" %(countVeh, numberOfVehicles))
        vehicleTimesDict = {}
        nxStartNode = vehicleObject.startNode
        nxEndNode = vehicleObject.endNode
        gtEdgeId = GtNetwork.nxToGtEdgesDict[(nxStartNode, nxEndNode)]
        edgeWeight = GtNetwork.gtEdgeWeights[gtEdgeId]
        # edgeWeight = float(G[startNode][endNode]['weight'])
        for facilityKey,_ in parameters.facilitiesDict.items():
            countFac += 1
            print("\tChecking facility %d out of %d" % (countFac, numberOfFacilities))
            distance1 = gt.shortest_distance(GtNetwork.Ggt, source = GtNetwork.nxToGtNodesDict[nxStartNode], target=GtNetwork.nxToGtNodesDict[facilityKey], weights=GtNetwork.gtEdgeWeights)
            time1 = edgeWeight * vehicleObject.pointInEdge + distance1 / beta[timeOfDay]
            distance2 = gt.shortest_distance(GtNetwork.Ggt, source = GtNetwork.nxToGtNodesDict[nxEndNode], target=GtNetwork.nxToGtNodesDict[facilityKey], weights=GtNetwork.gtEdgeWeights)
            time2 = edgeWeight * vehicleObject.pointInEdge + distance2 / beta[timeOfDay]
            tripTime = min(time1, time2)
            vehicleTimesDict[facilityKey] = tripTime
        timesDict[vehicleKey] = vehicleTimesDict
    return timesDict


def parallelUpdateVehiclesTimesDict(GtNetwork, parameters, timesDict, vehicleKeysList):
    numberOfVehicles = len(vehicleKeysList)
    countVeh = 0
    proc_id = getpid()
    for vehicleKey in vehicleKeysList:
        countVeh += 1
        print(f"Checking vehicle {countVeh} from total {numberOfVehicles} at process {proc_id}")
        vehicleObject = parameters.vehiclesDict[vehicleKey]
        numberOfFacilities = len(parameters.facilitiesDict.items())
        beta = [1]
        timeOfDay = 0            # time of a day (24*60 entries) counted in minutes starting from 0:00 and ending in 23:59
        countFac = 0
        vehicleTimesDict = {}
        nxStartNode = vehicleObject.startNode
        nxEndNode = vehicleObject.endNode
        gtEdgeId = GtNetwork.nxToGtEdgesDict[(nxStartNode, nxEndNode)]
        edgeWeight = GtNetwork.gtEdgeWeights[gtEdgeId]
        for facilityKey, _ in parameters.facilitiesDict.items():
            countFac += 1
            print("\tChecking facility %d out of %d at process %d" % (countFac, numberOfFacilities, proc_id))
            distance1 = gt.shortest_distance(GtNetwork.Ggt, source=GtNetwork.nxToGtNodesDict[nxStartNode],
                                             target=GtNetwork.nxToGtNodesDict[facilityKey], weights=GtNetwork.gtEdgeWeights)
            time1 = edgeWeight * vehicleObject.pointInEdge + distance1 / beta[timeOfDay]
            distance2 = gt.shortest_distance(GtNetwork.Ggt, source=GtNetwork.nxToGtNodesDict[nxEndNode],
                                             target=GtNetwork.nxToGtNodesDict[facilityKey], weights=GtNetwork.gtEdgeWeights)
            time2 = edgeWeight * vehicleObject.pointInEdge + distance2 / beta[timeOfDay]
            tripTime = min(time1, time2)
            vehicleTimesDict[facilityKey] = tripTime
        timesDict[vehicleKey] = vehicleTimesDict


def getTimeDictGtParallel(GtNetwork, parameters):
    print("Calculating parallel Gt trip times ...")
    processes = []
    numberOfVehicles = len(parameters.vehiclesDict.items())
    numberOfProcesses = cpu_count()
    vehiclesPerProcess = floor(numberOfVehicles / numberOfProcesses)
    vehiclesKeys = list(parameters.vehiclesDict.keys())
    manager = Manager()
    timesDict = manager.dict()
    for i in range(numberOfProcesses):
        start = i * vehiclesPerProcess
        if i < numberOfProcesses - 1:
            end = (i+1) * vehiclesPerProcess
        else:
            end = len(vehiclesKeys)
        process = Process(target=parallelUpdateVehiclesTimesDict, args=(GtNetwork, parameters, timesDict, vehiclesKeys[start:end]))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    return timesDict

def exportDeterministicTripTimes(timesDict, filename):
    print("Exporting trip times ...")
    fp = open(filename,"w")
    for vehicleKey, vehicleFacilityDict in timesDict.items():
        for facilityKey, vehicleFacilityTime in vehicleFacilityDict.items():
            fp.write("%s, %s, %s\n" %(vehicleKey, facilityKey, vehicleFacilityTime))
    fp.close()


# def getDistMatrix(G, facilities, vehicles):
#     parameters = pam.Parameters()
#     distMatrix = [ [0] * parameters.Nof ] * parameters.Nov
#     for i in range(parameters.Nov):
#         vclLocationList = vehicles[i].location
#         for j in range(parameters.Nof):
#             facLocation = facilities[j].location
#             expDist = 0
#             for scenario in range(len(vclLocationList)):
#                 vclLocation = vclLocationList[scenario]
#                 edgeLocation = vclLocation[0][0]
#                 edgePoint = vclLocation[1]
#                 edgeOrigin = edgeLocation[0]
#                 edgeDestination = edgeLocation[1]
#                 edgeWeight = G[edgeOrigin][edgeDestination]['weight']
                
#                 distance1 = edgeWeight * edgePoint + parameters.beta[i][j] * parameters.ps[scenario] *\
#                 nx.shortest_path_length(G, source=edgeOrigin, target=facLocation, weight='weight')

#                 distance2 = edgeWeight * (1 - edgePoint) + parameters.beta[i][j] * parameters.ps[scenario] *\
#                 nx.shortest_path_length(G, source=edgeDestination, target=facLocation, weight='weight')

#                 dist = min(distance1, distance2)
#                 expDist += dist
#             distMatrix[i][j] = expDist
#     return distMatrix



# from math import sin, cos, sqrt, atan2, radians
# def calculateDistanceInKm(latitude1, longitude1, latitude2, longitude2):
#     # approximate radius of earth in km
#     R = 6373.0
#
#     lat1 = radians(latitude1)
#     lon1 = radians(longitude1)
#     lat2 = radians(latitude2)
#     lon2 = radians(longitude2)
#
#     dlon = lon2 - lon1
#     dlat = lat2 - lat1
#
#     a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))
#
#     distance = R * c
#     return distance
#





# latitude1 = 43.6128279174
# longitude1 = -96.7704197366
# latitude2 = 43.5293061262
# longitude2 = -96.7510354923
# calculateDistance(latitude1, longitude1, latitude2, longitude2)


# distMatrix = getDistMatrix()
# print(distMatrix)
