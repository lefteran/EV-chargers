import networkx as nx
import graph_tool.all as gt
from math import floor
from multiprocessing import Process, Manager
from os import getpid, cpu_count
import settings
from serializationIO import printProgress


def getTimeDictNx(Gnx):
    print("Calculating Nx trip times ...")
    timesDict = {}
    beta = [1]
    timeOfDay = 0            # time of a day (24*60 entries) counted in minutes starting from 0:00 and ending in 23:59
    numberOfVehicles = len(settings.parameters.vehiclesDict.items())
    numberOfFacilities = len(settings.parameters.facilitiesDict.items())
    countVeh = 0
    for vehicleKey, vehicleObject in settings.parameters.vehiclesDict.items():
        countVeh += 1
        countFac = 0
        print("Checking vehicle %d out of %d" %(countVeh, numberOfVehicles))
        vehicleTimesDict = {}
        startNode = vehicleObject.startNode
        endNode = vehicleObject.endNode
        edgeWeight = float(Gnx[startNode][endNode]['weight'])
        for facilityKey,_ in settings.parameters.facilitiesDict.items():
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


def getTimeDictGt(GtNetwork):
    # TODO: if the vehicle-facility time is more than T set it to float("inf")
    print("Calculating Gt trip times ...")
    timesDict = {}
    beta = [1]
    timeOfDay = 0            # time of a day (24*60 entries) counted in minutes starting from 0:00 and ending in 23:59
    numberOfVehicles = len(settings.parameters.vehiclesDict.items())
    numberOfFacilities = len(settings.parameters.facilitiesDict.items())
    countVeh = 0
    for vehicleKey, vehicleObject in settings.parameters.vehiclesDict.items():
        countVeh += 1
        countFac = 0
        print("Checking vehicle %d out of %d" %(countVeh, numberOfVehicles))
        vehicleTimesDict = {}
        nxStartNode = vehicleObject.startNode
        nxEndNode = vehicleObject.endNode
        gtEdgeId = GtNetwork.nxToGtEdgesDict[(nxStartNode, nxEndNode)]
        edgeWeight = GtNetwork.gtEdgeWeights[gtEdgeId]
        # edgeWeight = float(G[startNode][endNode]['weight'])
        for facilityKey,_ in settings.parameters.facilitiesDict.items():
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


def parallelUpdateVehiclesTimesDict(GtNetwork, timesDict, vehicleKeysList):
    numberOfVehicles = len(vehicleKeysList)
    countVeh = 0
    proc_id = getpid()
    for vehicleKey in vehicleKeysList:
        countVeh += 1
        # print(f"Checking vehicle {countVeh} from total {numberOfVehicles} at process {proc_id}")
        vehicleObject = settings.parameters.vehiclesDict[vehicleKey]
        numberOfFacilities = len(settings.parameters.facilitiesDict.items())
        beta = [1]
        timeOfDay = 0            # time of a day (24*60 entries) counted in minutes starting from 0:00 and ending in 23:59
        countFac = 0
        vehicleTimesDict = {}
        nxStartNode = vehicleObject.startNode
        nxEndNode = vehicleObject.endNode
        gtEdgeId = GtNetwork.nxToGtEdgesDict[(nxStartNode, nxEndNode)]
        edgeWeight = GtNetwork.gtEdgeWeights[gtEdgeId]
        for facilityKey, _ in settings.parameters.facilitiesDict.items():
            countFac += 1
            # print("\tChecking facility %d out of %d at process %d" % (countFac, numberOfFacilities, proc_id))
            distance1 = gt.shortest_distance(GtNetwork.Ggt, source=GtNetwork.nxToGtNodesDict[nxStartNode],
                                             target=GtNetwork.nxToGtNodesDict[facilityKey], weights=GtNetwork.gtEdgeWeights)
            time1 = edgeWeight * vehicleObject.pointInEdge + distance1 / beta[timeOfDay]
            distance2 = gt.shortest_distance(GtNetwork.Ggt, source=GtNetwork.nxToGtNodesDict[nxEndNode],
                                             target=GtNetwork.nxToGtNodesDict[facilityKey], weights=GtNetwork.gtEdgeWeights)
            time2 = edgeWeight * vehicleObject.pointInEdge + distance2 / beta[timeOfDay]
            tripTime = min(time1, time2)
            vehicleTimesDict[facilityKey] = tripTime
        percentage = float(countVeh) / float(numberOfVehicles)
        printProgress(percentage)
        timesDict[vehicleKey] = vehicleTimesDict


def getTimeDictGtParallel(GtNetwork):
    print("Calculating parallel Gt trip times ...")
    processes = []
    numberOfVehicles = len(settings.parameters.vehiclesDict.items())
    numberOfProcesses = cpu_count()
    vehiclesPerProcess = floor(numberOfVehicles / numberOfProcesses)
    vehiclesKeys = list(settings.parameters.vehiclesDict.keys())
    manager = Manager()
    timesDict = manager.dict()
    for i in range(numberOfProcesses):
        start = i * vehiclesPerProcess
        if i < numberOfProcesses - 1:
            end = (i+1) * vehiclesPerProcess
        else:
            end = len(vehiclesKeys)
        process = Process(target=parallelUpdateVehiclesTimesDict, args=(GtNetwork, timesDict, vehiclesKeys[start:end]))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    return timesDict

