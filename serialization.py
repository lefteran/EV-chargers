import jsonpickle
import json

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