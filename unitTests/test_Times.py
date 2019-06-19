import unittest
import importData as impdt

class TestTimesDict(unittest.TestCase):
    def test_TimesDict(self):
        parameters = impdt.importNetworkAndDicts()
        finiteTimesCountList = [0] * len(parameters.vehiclesDict.items())
        vehicleCount = 0
        for vehicleKey, _ in parameters.vehiclesDict.items():
            for facilityKey, _ in parameters.facilitiesDict.items():
                if parameters.timesDict[vehicleKey][facilityKey] != float("inf"):
                    finiteTimesCountList[vehicleCount] += 1
            self.assertGreater(finiteTimesCountList[vehicleCount], 0)
            vehicleCount += 1
        a=2



