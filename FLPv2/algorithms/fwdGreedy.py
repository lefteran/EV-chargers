# LIBRARIES
import _pickle as pickle
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



def get_total_time_with_new_location(solution, location):
    total_time = 0
    for vehicle_location in settings.vehicles_locations_over_day:
        new_solution = solution[:]
        new_solution.append(location)
        total_time += get_vehicle_time_to_nearest_location(vehicle_location, new_solution)
    return total_time

#
# def add_most_important_location(S, previous_total_time):
#     totalTime = previous_total_time
#     min_time_location = None
#     for facilityId in settings.candidateLocations:
#         if facilityId not in S:
#             timeWithNewFacility = get_time_with_new_facility(S, facilityId)
#             if timeWithNewFacility < totalTime:
#                 totalTime = timeWithNewFacility
#                 min_time_location = facilityId
#     if min_time_location is not None:
#         S.append(min_time_location)
#     return totalTime


def add_most_important_location(solution, previous_total_time):
    total_time = previous_total_time
    min_time_location = None
    for location in settings.clusters.keys():
        if location not in solution:
            time_to_new_location = get_total_time_with_new_location(solution, location)
            if time_to_new_location < total_time:
                total_time = time_to_new_location
                min_time_location = location
    if min_time_location is not None:
        solution.append(min_time_location)
    return total_time


def forward_greedy():
    print(f"Running forward greedy with {settings.fleet_size} vehicles and {settings.centroids} clusters ...")
    solution = []
    total_driving_time = float("inf")

    for _ in tqdm(range(settings.k)):
        previous_total_driving_time = total_driving_time
        total_driving_time = add_most_important_location(solution, previous_total_driving_time)
        if len(solution) == len(settings.vehicles_locations_over_day):
            return solution, total_driving_time
    return solution, total_driving_time



