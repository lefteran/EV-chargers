from math import ceil
import json
from os import listdir


def exportResultsFromJsonToCsv():
    runs = 1
    for i in range(runs):
        runNo = 'run_' + str(i+1)
        tuplesList = []
        radius = 0.2
        # algorithm = 'rndLocalSearch_'
        # algorithm = 'fwdGreedy_'
        # algorithm = 'optimal_'
        algorithm = 'localSearch_'
        # directoryPath = 'D:\Github\EV-chargers\FLP\data\solutions\\randomLocalSearch\k_50\p_3\\r_10000\\' + runNo
        directoryPath = 'D:\Github\EV-chargers\FLP\data\solutions\localSearch\k_50\\0.2\p_1\\'
        fpCsv = open(directoryPath + '\\results-' + runNo + '.csv', 'w')
        filenamesList = listdir(directoryPath)
        for filename in filenamesList:
            if filename.endswith('.json'):
                numberOfVehicles = int(filename[filename.find(algorithm) + len(algorithm): filename.rfind('_' + str(radius) + '.json')])
                filePath = directoryPath + '\\' + filename
                with open(filePath) as fp:
                    data = json.load(fp)
                    objective = ceil(float(data['cost']))
                    runtime = ceil(float(data['time']))
                tuplesList.append((numberOfVehicles, objective, runtime))
        tuplesList.sort(key=lambda tup: tup[0])
        for mytuple in tuplesList:
            # print(f'{mytuple[0]}, {mytuple[1]}, {mytuple[2]}\n')
            fpCsv.write(f'{mytuple[0]}, {mytuple[1]}, {mytuple[2]}\n')
        fpCsv.close()



exportResultsFromJsonToCsv()