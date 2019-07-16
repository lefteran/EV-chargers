import solution.initialise as intl
import solution.local_search as ls
import solution.parallelisation.localSearchPrl as pls
import _pickle as pickle

def getUnbudgetedSolution(parameters):
    lambdaVal = 0
    initSol = intl.initialiseSolution(parameters)
    initialSolution = pickle.loads(pickle.dumps(initSol, -1))
    if parameters.parallelLocalSearch:
        localSearchSolution = pls.distributeZonesToProcesses(initSol, parameters, lambdaVal)
    else:
        localSearchSolution = ls.localSearch(initSol, parameters, lambdaVal)
    return initialSolution, localSearchSolution

