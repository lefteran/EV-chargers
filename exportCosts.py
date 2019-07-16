def exportCosts(filename, parameters, initialSolutionCost, localSearchCost):
    with open(filename, "a") as exportFile:
        exportFile.write(f"Initial cost: {initialSolutionCost}. Local search cost: {localSearchCost}. Number of swaps: {parameters.swaps}\n")
