import i_o.serializationIO as serializationIO




candidatesCoordinates = serializationIO.importAndDeserialize('candidatesCoordinates.json')
solutionCoordinates = serializationIO.importAndDeserialize('solutionCoordinates.json')


fpCandidates = open('candidates.csv', 'w')
for node in candidatesCoordinates:
    fpCandidates.write(f'{node[0]}, {node[1]}\n')
fpCandidates.close()


fpSolution = open('solution.csv', 'w')
for node in solutionCoordinates:
    fpSolution.write(f'{node[0]}, {node[1]}\n')
fpSolution.close()