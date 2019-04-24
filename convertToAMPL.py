# import math

def convertToAMPL(parameters):
	amplDataFile = "amplData.dat"
	fp = open(amplDataFile,"w")
	fp.write("# CFP data AMPL format\n\n")

	fp.write("set F := ")
	for facility in parameters.facilities:
		fp.write("%d " %(facility.id + 1))
	fp.write(";\n")

	fp.write("set Z := ")
	for zone in parameters.zones:
		fp.write("%d " %(zone.id + 1))
	fp.write(";\n")

	fp.write("set V := ")
	for vehicle in parameters.vehicles:
		fp.write("%d " %(vehicle.id + 1))
	fp.write(";\n\n")

	fp.write("set C := ")
	maxCapacity = max(facility.capacity for facility in parameters.facilities)
	for capacity in range(maxCapacity):
		fp.write("%d " %(capacity + 1))
	fp.write(";\n\n")	

	# IF log(C) + 1 DIGITS ARE USED
	# fp.write("set C := ")
	# maxCapacity = max(facility.capacity for facility in parameters.facilities)
	# maxLogCapacity = math.floor(math.log(maxCapacity,2)) + 1
	# for capacity in range(maxLogCapacity):
	# 	fp.write("%d " %(capacity + 1))
	# fp.write(";\n\n")	


	fp.write("param a :=\n")
	for facility in parameters.facilities:
		fp.write("%d %d\n" %(facility.id + 1, facility.alpha))
	fp.write(";\n\n")

	fp.write("param H :=\n")
	for j in range(len(parameters.facilities)):
		for z in range(len(parameters.zones)):
			if parameters.belonging[j] == z:
				fp.write("%d %d 1\n" %(j+1, z+1))
			else:
				fp.write("%d %d 0\n" %(j+1, z+1))
	fp.write(";\n\n")

	fp.write("param A :=\n")
	zonesLen = len(parameters.zones)
	for z in range(zonesLen):
		for zeta in range(zonesLen):
			if (z == zeta) or (zeta in parameters.adjMatrix[z]):
				fp.write("%d %d 1\n" %(z+1, zeta+1))
			else:
				fp.write("%d %d 0\n" %(z+1, zeta+1))
	fp.write(";\n\n")


	fp.write("param dem :=\n")
	for z in range(len(parameters.zones)):
		fp.write("%d %d\n" %(z+1, parameters.zones[z].demand))
	fp.write(";\n\n")

	fp.write("param Nz :=\n")
	for z in range(len(parameters.zones)):
		fp.write("%d %d\n" %(z+1, parameters.zones[z].onStreetBound))
	fp.write(";\n\n")

	fp.write("param c :=\n")
	for facId in range(len(parameters.facilities)):
		fp.write("%d %d\n" %(facId+1, parameters.c[facId]))
	fp.write(";\n\n")

	fp.write("param cap :=\n")
	for facId in range(len(parameters.facilities)):
		fp.write("%d %d\n" %(facId+1, parameters.facilities[facId].capacity))
	fp.write(";\n\n")

	fp.write("param dist :=\n")
	for i in range(parameters.Nov):
		for j in range(parameters.Nof):
			fp.write("%d %d %f\n" %(i+1, j+1, parameters.distMatrix[i][j]))
	fp.write(";\n\n")

	fp.write("param B :=\n" + str(parameters.B) + "\n")
	fp.write(";\n\n")

	fp.write("param R :=\n" + str(parameters.R) + "\n")
	fp.write(";\n\n")

	fp.write("param cst :=\n" + str(parameters.cst) + "\n")
	fp.write(";\n\n")

	fp.write("param cr :=\n" + str(parameters.cr) + "\n")
	fp.write(";\n\n")

	fp.write("param gamma :=\n" + str(parameters.gamma) + "\n")
	fp.write(";\n\n")


	fp.close()