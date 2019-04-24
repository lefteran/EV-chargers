import initialise as intl
import local_search as ls


def getSolution(parameters, lambdaVal):
    initSol = intl.initialise(parameters, lambdaVal)
    sol = ls.localSearch(initSol, parameters, lambdaVal)
    return sol

def lagrangian(parameters):
    lambda1 = 0
    lambda2 = parameters.lambdaMax
    lambdaVal = lambda1
    bestSol = getSolution(parameters, lambdaVal)
    bestCost = bestSol.getCostLagrangian(parameters, lambdaVal)
    bestLambda = lambda1
    lambdaVal = lambda2
    while lambda2 - lambda1 > parameters.epsilon:
        sol = getSolution(parameters, lambdaVal)
        solCost = sol.getCostLagrangian(parameters, lambdaVal)
        if sol.IsFeasibleWithBudget(parameters):
            if solCost > bestCost:
                bestSol = sol
                bestCost = solCost
                bestLambda = lambdaVal
                print("------------------ LOCAL SEARCH (lambda = %.2f) ----------------------" %lambdaVal)
                bestSol.printSol(parameters, lambda1)
            lambdaVal = (lambda2 + lambda1) / 2
            lambda1 = lambdaVal
        else:
            lambdaVal = (lambda2 + lambda1) / 2
            lambda2 = lambdaVal
            
    print("-------- BEST SOLUTION (lambda = %.2f) ---------------" %bestLambda)
    bestSol.printSol(parameters, bestLambda)


    