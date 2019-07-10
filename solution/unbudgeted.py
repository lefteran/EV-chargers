import solution.initialise as intl
import solution.local_search as ls


def getUnbudgetedSolution(parameters):
    lambdaVal = 0
    initSol = intl.initialiseSolution(parameters)
    # sol = ls.localSearch(initSol, parameters, lambdaVal)
    return initSol  # CHECK THE RETURNED VALUE!!!!!!!!!!

