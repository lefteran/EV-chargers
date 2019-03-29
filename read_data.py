import parameters as pam
import zone as zn
import facility as fl

def read_data():
	parameters = pam.Parameters()
	
	zonesFile = "zone_data.txt"
	fpz = open(zonesFile,"r")
	next(fpz)
	next(fpz)
	zones = []
	linesNum = 0
	for line in fpz:
		linesNum += 1
		elements = line.split("\t")
		idNum = int(elements[0])
		adjacent = elements[1]
		demand = int(elements[2])
		facilities = elements[3]
		zone = zn.Zone(idNum, adjacent, demand, facilities)
		zones.append(zone)
	if parameters.Noz != linesNum:
		print("The number of lines in zone_data file is not equal to Noz given in parameters")
	fpz.close()

	facilitiesFile = "facilitiy_data.txt"
	fpf = open(facilitiesFile,"r")
	next(fpf)
	next(fpf)
	facilities = []
	linesNum = 0
	for line in fpf:
		linesNum += 1
		elements = line.split("\t")
		idNum = int(elements[0])
		cost = float(elements[1])
		capacity = int(elements[2])
		alpha = int(elements[3])
		zone = int(elements[4])
		facility = fl.Facility(idNum, cost, capacity, alpha, zone)
		facilities.append(facility)
	if parameters.Nof != linesNum:
		print("The number of lines in facility_data file is not equal to Nof given in parameters")
	fpf.close()
	return zones, facilities


# zones, facilities = read_data()
# for z in zones:
# 	print("zone id is %d and demand is %d" %(z.id, z.demand))
# 	print("zone adjacent zones are ", z.adjacent)
# for j in facilities:
# 	print("facility id is %d and cost is %f" %(j.id, j.cost))