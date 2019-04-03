import parameters as pam
import zone as zn
import vehicle as vcl
import facility as fl

# the index of a cell corresponds to the id of the facility and its value to the zone it belongs to
def getBelongingList():
	parameters = pam.Parameters()
	belongingFile = "belonging.txt"
	fpb = open(belongingFile,"r")
	for i in range(3):
		next(fpb)
	belonging = [0] * parameters.Nof
	zonesNum = 0
	for zone in fpb:
		elements = zone.split("\t")
		if parameters.Nof != len(elements) - 1:
			print("*** The number of columns in the belonging.txt file is not equal to Nof given in parameters ***")
		for i in range(len(elements) - 1):
			if int(elements[i+1]) == 1:
				belonging[i] = zonesNum
		zonesNum += 1
	fpb.close()
	return belonging


def getAdjMatrix():
	parameters = pam.Parameters()
	adjecencyFile = "adjacent_zones.txt"
	fpa = open(adjecencyFile,"r")
	for i in range(2):
		next(fpa)
	adjacencyMatrix = [ [] for l in range(parameters.Noz) ]
	adjZonesNum = 0
	for zone in fpa:
		elements = zone.split("\t")
		if parameters.Noz != len(elements) - 1:
			print("The number of columns in adjacent_zones.txt file is not equal to Noz given in parameters")
		for i in range(len(elements) - 1):
			if(int(elements[i+1]) == 1):
				adjacencyMatrix[adjZonesNum].append(i)
		adjZonesNum += 1
	fpa.close()
	return adjacencyMatrix

def getFacilities():
	parameters = pam.Parameters()
	belonging = getBelongingList()
	facilitiesFile = "facilitiy_data.txt"
	fpf = open(facilitiesFile,"r")
	next(fpf)
	facilities = []
	linesNum = 0
	for line in fpf:
		elements = line.split("\t")
		idNum = linesNum
		cost = float(elements[1])
		capacity = int(elements[2])
		alpha = int(elements[3])
		zone = belonging[linesNum]
		location = int(elements[4])
		facility = fl.Facility(idNum, location, cost, capacity, alpha, zone)
		facilities.append(facility)
		linesNum += 1
	if parameters.Nof != linesNum:
		print("The number of lines in facility_data file is not equal to Nof given in parameters")
	fpf.close()
	return facilities


def getZones():
	parameters = pam.Parameters()
	adjacencyMatrix = getAdjMatrix()
	zonesFile = "zone_data.txt"
	fpz = open(zonesFile,"r")
	next(fpz)
	zones = []
	linesNum = 0
	for line in fpz:
		elements = line.split("\t")
		idNum = int(elements[0])
		adjacent = adjacencyMatrix[idNum]
		demand = int(elements[1])
		zoneFacilities = []
		for facility in facilities:
			if facility.zone == idNum:
				zoneFacilities.append(facility)
		onStreetBound = int(elements[2])
		zone = zn.Zone(idNum, adjacent, demand, zoneFacilities, onStreetBound)
		zones.append(zone)
		linesNum += 1
	if parameters.Noz != linesNum:
		print("The number of lines in zone_data file is not equal to Noz given in parameters")
	fpz.close()
	return zones


def getVehicles():
	parameters = pam.Parameters()
	vehiclesFile = "vehicle_data.txt"
	fpv = open(vehiclesFile,"r")
	next(fpv)
	vehicles = []
	linesNum = 0
	for line in fpv:
		locations = []
		elements = line.split("\t")
		idNum = int(elements[0])
		for i in range(len(elements) - 1):
			locations.append(int(elements[i+1]))
		vehicle = vcl.Vehicle(idNum, locations)
		vehicles.append(vehicle)
		linesNum += 1
	if parameters.Nos != len(elements) - 1:
		print("The number of possible locations of a vehicle in vehicle_data.txt file is not equal to Nos given in parameters")
	if parameters.Nov != linesNum:
		print("The number of lines in vehicle_data.txt file is not equal to Nov given in parameters")
	fpv.close()
	return vehicles

belonging = getBelongingList()
AdjMatrix = getAdjMatrix()
facilities = getFacilities()
zones = getZones()
vehicles = getVehicles()






# for i in range(len(vehicles)):
# 	print(vehicles[i].location)
# # print("adjacencyMatrix is ", AdjMatrix)
# # print("belonging is ", belonging)
# # for facility in facilities:
# # 		print("facility is %d and zone it belongs to is %d" %(facility.id, facility.zone))
# for zone in zones:
# 	print("zone is %d and  adjacent nodes are ")
# 	print(zone.adjacent)
# 	print(" and facilities are ")


# zones, facilities = read_data()
# for z in zones:
# 	print("zone id is %d and demand is %d" %(z.id, z.demand))
# 	print("zone adjacent zones are ", z.adjacent)
# for j in facilities:
# 	print("facility id is %d and cost is %f" %(j.id, j.cost))