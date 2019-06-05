import solution.initialise as intl
import solution.local_search as ls

def getSolution(importSol, parameters, lambdaVal):
    initSol = intl.initialiseSolution(importSol, parameters, lambdaVal)
    sol = ls.localSearch(initSol, parameters, lambdaVal)
    return sol

def lagrangianRelaxation(importSol, parameters):
    lambda1 = 0
    lambda2 = parameters.lambdaMax
    lambdaVal = lambda1
    bestSol = getSolution(importSol, parameters, lambdaVal)
    bestCost = bestSol.getLagrangianCost(parameters, lambdaVal)
    # bestLambda = lambda1
    # lambdaVal = lambda2
    # while lambda2 - lambda1 > parameters.epsilon:
    #     sol = getSolution(importSol, parameters, lambdaVal)
    #     solCost = sol.getLagrangianCost(parameters, lambdaVal)
    #     if sol.IsFeasibleWithBudget(parameters):
    #         if solCost > bestCost:
    #             bestSol = sol
    #             bestCost = solCost
    #             bestLambda = lambdaVal
    #             print("------------------ LOCAL SEARCH (lambda = %.2f) ----------------------" %lambdaVal)
    #             bestSol.printSol(parameters, lambda1)
    #         lambdaVal = (lambda2 + lambda1) / 2
    #         lambda1 = lambdaVal
    #     else:
    #         lambdaVal = (lambda2 + lambda1) / 2
    #         lambda2 = lambdaVal
            
    # print("-------- BEST SOLUTION (lambda = %.2f) ---------------" %bestLambda)
    # bestSol.printSol(parameters, bestLambda)
    return bestCost


    