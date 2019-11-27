import unittest
import importData as impdt
import Parameters
import GraphToolNetwork as gtn

class TestTimesDict(unittest.TestCase):
    # METHODS MUST BEGIN WITH THE WORD test!!!!!!!!!!
    def test_TimesDict(self):
        parameters = Parameters.Parameters()
        Gnx = impdt.importNetwork(parameters)
        GtNetwork = gtn.GraphToolNetwork()
        GtNetwork.createGraphToolNetworkFromGnx(Gnx)
        impdt.getVehicles(Gnx, parameters)
        impdt.getTimes(Gnx, GtNetwork, parameters)

        finiteTimesCountList = [0] * len(parameters.vehiclesDict.items())
        vehicleCount = 0
        for vehicleKey, _ in parameters.vehiclesDict.items():
            for facilityKey, _ in parameters.facilitiesDict.items():
                if parameters.timesDict[vehicleKey][facilityKey] != float("inf"):
                    finiteTimesCountList[vehicleCount] += 1
            self.assertGreater(finiteTimesCountList[vehicleCount], 0)
            vehicleCount += 1
        a=2



