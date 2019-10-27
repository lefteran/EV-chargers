# LIBRARIES
import json
from tqdm import tqdm
# FILES
import settings


def get_vehicle_time_to_nearest_location(vehicle_location, locations):
    time_to_nearest_location = float("inf")
    for candidate_location in locations:
        travel_time = settings.travel_times_over_day[str(vehicle_location) + '-' + str(candidate_location)]
        if travel_time < time_to_nearest_location:
            time_to_nearest_location = travel_time
    return time_to_nearest_location


def get_solution_time(solution):
    total_time = 0
    for vehicle_location in settings.vehicles_locations_over_day:
        total_time += get_vehicle_time_to_nearest_location(vehicle_location, solution)
    return total_time




def local_search(solution):
    print(f"Running local search with {settings.fleet_size} vehicles and {settings.centroids} clusters ...")
    best_time = get_solution_time(solution)

    closed = list(set(settings.clusters.keys()).difference(set(solution)))      # needs to go before the "for closed_facility in closed"
    flag = True                                                                 # loop since closed list is updated
    # previous_solution_accepted = False
    combinations_used = []


    iterations_count = 0
    while flag:
        print(f'number of iterations: {iterations_count}')
        better_solution = False
        for open_facility in tqdm(solution):
            for closed_facility in closed:
                if {open_facility, closed_facility} not in combinations_used:
                    candidate_solution = solution[:]
                    candidate_solution.remove(open_facility)
                    candidate_solution.append(closed_facility)
                    new_time = get_solution_time(candidate_solution)
                    # previous_solution_accepted = False
                    if new_time < best_time:
                        combinations_used.append({open_facility, closed_facility})
                        # previous_solution_accepted = True
                        solution = candidate_solution
                        best_time = new_time
                        better_solution = True
                        break
            if better_solution:
                break
        if not better_solution:
            return solution, best_time
        iterations_count += 1






    return solution, best_time











def localSearch1():                 # MODIFY THE ABOVE ALGORITHM HERE TO ALLOW GENERALISATION FOR p=2,3. TRY FIRST WITH
                                    # p=1 TO VERIFY IT GIVES THE SAME SOLUTION. TAKE ALL THE POSSIBLE COMBINATIONS OF OPEN
                                    # AND CLOSED FACILITIES
    print(f"Running local search with {settings.numberOfVehicles} vehicles and {settings.radius} radius ...")
    for _, vehicleObject in settings.vehiclesDict.items():
        vehicleObject.createSortedListOfTuplesAndDictOfIndices()

    solObject = serializationIO.importAndDeserialize(settings.fwdGreedyFile)
    S = solObject.solutionList
    bestTime = solObject.cost
    Closed = list(set(settings.candidateLocations).difference(set(S)))
    flag = True

    while flag:
        betterSolution = False
        for openFacility in S:
            for closedFacility in Closed:
                candidateSol = pickle.loads(pickle.dumps(S, -1))
                candidateSol.remove(openFacility)
                candidateSol.append(closedFacility)
                newTime = computeTime(candidateSol, closedFacility, openFacility)
                if newTime < bestTime:
                    S = candidateSol
                    bestTime = newTime
                    betterSolution = True
                    break
            if betterSolution:
                break
        if not betterSolution:
            return S, bestTime


