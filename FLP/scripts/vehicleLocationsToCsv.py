import i_o.serializationIO as serializationIO
import json
from math import sin, cos, sqrt, atan2, radians


def distanceInKm(latitude1, longitude1, latitude2, longitude2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(latitude1)
    lon1 = radians(longitude1)
    lat2 = radians(latitude2)
    lon2 = radians(longitude2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance



vehiclesDict = serializationIO.importAndDeserialize('vehiclesDict_1000.json')
with open('ChicagoNodes.geojson') as fn:
    data = json.load(fn)
fp = open('vehiclesLocations.csv', "w")
fp.write('vehicleLatitude, vehicleLongitude, startNodeId, startNodeLat, startNodeLon, endNodeId, endNodeLat, endNodeLon\n')
for _, vehicleValue in vehiclesDict.items():
    startNodeId = int(vehicleValue['startNode'])
    endNodeId = int(vehicleValue['endNode'])
    pointInEdge = vehicleValue['pointInEdge']
    startNodeFound = False
    endNodeFound = False
    startNodeLat = -1
    startNodeLon = -1
    endNodeLat = -1
    endNodeLon = -1
    for feature in data['features']:
        nodeId = int(feature['properties']['identifier'])
        if nodeId == startNodeId:
            coordinates = feature['geometry']['coordinates']
            startNodeLat = coordinates[0]
            startNodeLon = coordinates[1]
            startNodeFound = True
        if nodeId == endNodeId:
            coordinates = feature['geometry']['coordinates']
            endNodeLat = coordinates[0]
            endNodeLon = coordinates[1]
            endNodeFound = True
        if startNodeFound and endNodeFound:
            break
    vehicleLat = (1 - pointInEdge) * startNodeLat + pointInEdge * endNodeLat
    vehicleLon = (1 - pointInEdge) * startNodeLon + pointInEdge * endNodeLon

    fp.write(f'{vehicleLat}, {vehicleLon}, {startNodeId}, {startNodeLat}, {startNodeLon}, {endNodeId}, {endNodeLat}, {endNodeLon}\n')
fp.close()