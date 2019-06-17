import solution.initialise as intl
import solution.local_search as ls


def getUnbudgetedSolution(importSol, parameters):
    lambdaVal = 0
    initSol = intl.initialiseSolution(importSol, parameters)
    sol = ls.localSearch(initSol, parameters, lambdaVal)
    return sol  # CHECK THE RETURNED VALUE!!!!!!!!!!

