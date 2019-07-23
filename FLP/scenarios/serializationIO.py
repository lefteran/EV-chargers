import jsonpickle
import json
import os
from math import floor

def serializeAndExport(obj, filename):
    print(f"Serializing and exporting to {filename} ...")
    serializedObj = jsonpickle.encode(obj)
    with open(filename, 'w') as f:
        json.dump(serializedObj, f)


def importAndDeserialize(filename):
    print(f"Importing and deserializing input from {filename} ...")
    with open(filename) as json_file:
        importedData = json.load(json_file)
        obj = jsonpickle.decode(importedData)
    return obj


def exportDeterministicTripTimes(timesDict, filename):
    print("Exporting trip times ...")
    fp = open(filename,"w")
    for vehicleKey, vehicleFacilityDict in timesDict.items():
        for facilityKey, vehicleFacilityTime in vehicleFacilityDict.items():
            fp.write("%s, %s, %s\n" %(vehicleKey, facilityKey, vehicleFacilityTime))
    fp.close()


def printProgress(percentage):
    pid = os.getpid()
    value = floor(percentage * 10)
    print(f"Process: {pid}\nPercent: [{'#' * value}] {percentage * 100}%\n")