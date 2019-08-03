S=[10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160]

numberOfProcesses = 3
facilityKeysPerProcess = 4
for i in range(numberOfProcesses):
    first = i * facilityKeysPerProcess
    last = None if i == numberOfProcesses - 1 else first + facilityKeysPerProcess
    facilitiesToCheck = S[first:last]
    print(facilitiesToCheck)