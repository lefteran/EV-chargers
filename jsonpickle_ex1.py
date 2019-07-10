import jsonpickle
import vehicle as vh
import json

class ParametersTest:
    def __init__(self):
        self.facilitiesDict = {}
        self.zonesDict = {}
        self.vehiclesDict = {}
        self.belongingDict = {}
        self.adjacencyDict = {}
        self.timesDict = {}
        self.standardCost = 25
        self.rapidCost = 38
        self.budget = 400000000
        self.facilitiesNo = 0
        self.zonesNo = 0
        self.vehiclesNo = 0
        self.gamma = 0.5
        self.R = 10
        self.lambdaMax = 10
        self.epsilon = 2
        self.swaps = 1
        self.doPreprocessing = False
        self.importSolution = False
        self.importDeterministicTimes = False
        self.useGraphTool = True
        self.parallelComputationOfTimes = True
        self.exportParametersFlag = False
        self.importParametersFlag = True

    def importVehicleData(self, filename):
        vehicleDataDict = {}
        fp = open(filename, "r")
        for line in fp:
            elements = line.split(",")
            key = elements[0].strip()
            vehicleDataDict[key] = []
            for i in range(len(elements) - 1):
                vehicleDataDict[key].append(elements[i + 1].strip())
        fp.close()
        return vehicleDataDict

    def getVehicles(self):
        vehicleDataDict = self.importVehicleData('Chicago/VehicleData.csv')
        for vehicleId, vehicleDataList in vehicleDataDict.items():
            startNode = vehicleDataList[0]
            endNode = vehicleDataList[1]
            self.vehiclesDict[vehicleId] = vh.Vehicle(vehicleId, startNode, endNode, float(vehicleDataList[2]))


obj = ParametersTest()
obj.getVehicles()
serializedObj = jsonpickle.encode(obj)
with open('parametersTest.json', 'w') as f:
    json.dump(serializedObj, f)

with open('parametersTest.json') as json_file:
    importedData = json.load(json_file)
    thawed = jsonpickle.decode(importedData)
    a=2

# a=2
# thawed = jsonpickle.decode(frozen)
# a=3