import initialise as intl
import parameters as pam
import solution as sl

parameters = pam.Parameters()
initialSol = sl.Solution(parameters)
initialSol.set_values(parameters, [[1,1,0], [0,0,1]], [1,1,1], [0,1,3], [2,0,5], [2,1,8])
print("The cost of the objective function is %f" %initialSol.solutionCost(parameters))
value = initialSol.isFeasible(parameters)
print("Is S feasible: %r" %value)

sol = intl.initialise(parameters)