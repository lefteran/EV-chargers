def convertToAMPL(facilities, zones, vehicles, belonging, adjMatrix):
	amplDataFile = "amplData.dat"
	fp = open(amplDataFile,"w")
	fp.write("# CFP data AMPL format\n\n")

	fp.write("set F := ")
	for facility in facilities:
		fp.write("%d " %(facility.id + 1))
	fp.write(";\n")

	fp.write("set Z := ")
	for zone in zones:
		fp.write("%d " %(zone.id + 1))
	fp.write(";\n")

	fp.write("set V := ")
	for vehicle in vehicles:
		fp.write("%d " %(vehicle.id + 1))
	fp.write(";\n\n")

	fp.write("param a :=\n")
	for facility in facilities:
		fp.write("%d %d\n" %(facility.id + 1, facility.alpha))
	fp.write(";\n\n")

	fp.write("param H :=\n")
	for j in range(len(facilities)):
		for z in range(len(zones)):
			if belonging[j] == z:
				fp.write("%d %d 1\n" %(j+1, z+1))
			else:
				fp.write("%d %d 0\n" %(j+1, z+1))
	fp.write(";\n\n")

	fp.write("param A :=\n")
	for z in range(len(zones)):
		for zeta in range(len(zones)):
			if (z == zeta) or (zeta in adjMatrix[z]):
				fp.write("%d %d 1\n" %(z+1, zeta+1))
			else:
				fp.write("%d %d 0\n" %(z+1, zeta+1))
	fp.write(";\n\n")


	fp.close()