# LIBRARIES
import os
# FILES
import settings
import i_o.serializationIO as serializationIO



def convertCsvToDat():
    settings.resetFilePaths()
    vehiclesList = []
    optimalMapping = {}
    fpi = open(settings.timesDictFile ,"r")
    datFilename = os.path.splitext(settings.timesDictFile)[0] + '.dat'
    fpo = open(datFilename, "w")

    fpo.write(f'param k := {settings.k};\n\n\nparam t :=\n')

    facilityCount = 0
    for line in fpi:
        elements = line.split(",")
        vehicleId = elements[0].strip()
        facilityOriginalId = elements[1].strip()
        vehicleFacilityTime = float(elements[2].strip())
        if vehicleId not in vehiclesList:
            vehiclesList.append(vehicleId)
        if facilityOriginalId not in optimalMapping:
            facilityCount += 1
            optimalMapping[facilityOriginalId] = str(facilityCount)
        if vehicleFacilityTime != float("inf"):
            fpo.write(f'{vehicleId} {optimalMapping[facilityOriginalId]} {vehicleFacilityTime}\n')
    fpo.write(';\n\n\n')

    fpo.write('set V := ')
    vehiclesNumber = len(vehiclesList)
    for i in range(vehiclesNumber):
        fpo.write(f'{i};') if i == vehiclesNumber - 1 else fpo.write(f'{i} ')
    fpo.write('\n\n')

    fpo.write('set F := ')
    for i in range(facilityCount):
        fpo.write(f'{i+1};') if i == facilityCount - 1 else fpo.write(f'{i+1} ')

    serializationIO.serializeAndExport(optimalMapping, settings.optimalMapping)

    fpi.close()
    fpo.close()


# convertCsvToDat()