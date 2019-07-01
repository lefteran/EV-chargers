from multiprocessing import Value

class globalPartOfSolution:
	def __init__(self, parameters, S):
		self.x = {}
		for vehicleKey, _ in parameters.vehiclesDict.items():
			xFacilitiesDict = {}
			for facilityKey, _ in parameters.facilitiesDict.items():
				xFacilitiesDict[facilityKey] = Value('i', S.x[vehicleKey][facilityKey])
			self.x[vehicleKey] = xFacilitiesDict

