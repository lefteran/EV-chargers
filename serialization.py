import jsonpickle
import json

def serializeAndExport(obj, filename):
    serializedObj = jsonpickle.encode(obj)
    with open(filename, 'w') as f:
        json.dump(serializedObj, f)


def importAndDeserialize(filename):
    with open(filename) as json_file:
        importedData = json.load(json_file)
        obj = jsonpickle.decode(importedData)
    return obj