import time
import settings
import importData as impdt
import serializationIO
import fwdGreedy
import revGreedy
import solution
import jsonpickle

if __name__ == "__main__":
	start_time = time.time()
	settings.init()

	Gnx = impdt.importNetwork()

	print("Getting vehicles and vehicle-facility times ...")
	impdt.getVehicles()
	impdt.getTimes()

	algorithmDict = {1: "Forward Greedy",
					 2: "Reverse Greedy",
					 3: "Local Search"}
	algorithm = 2


	if algorithm == 1:
		S, totalCost = fwdGreedy.forwardGreedy()
	elif algorithm == 2:
		S, totalCost = revGreedy.reverseGreedy()
	else:
		# S, totalCost = unbudgeted.localSearch()
		S = []
		totalCost = -1

	solObject = solution.Solution(S, totalCost, algorithm, (time.time() - start_time))
	serializationIO.serializeAndExport(solObject, "solutions/fwdGreedy.json")

	print(f"S is {S} with cost = {totalCost}")

	print("--- %s seconds ---" % (time.time() - start_time))

