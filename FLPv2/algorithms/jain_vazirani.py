# LIBRARIES
from math import floor, ceil
import networkx as nx
from tqdm import tqdm
from time import sleep
from itertools import combinations
# FILES
import settings



# def phase1_unweighted():
#     # TODO Check the right value for max_alg_time
#     precision = 1000000
#     conflicts = dict()
#     max_alg_time = 10000000
#     temporarily_open = list()
#     sorted_times = sorted(settings.travel_times_over_day.items(), key=lambda kv: kv[1])
#     sorted_times = [(key, floor(travel_time * precision)) for (key, travel_time) in sorted_times if travel_time != 0]
#     unconnected_vehicles = settings.vehicles_locations_over_day[:]
#
#     for alg_time in tqdm(range(max_alg_time)):
#         edge_key = sorted_times[0][0]
#         vehicle_location = edge_key.split('-')[0]
#         candidate_location = edge_key.split('-')[1]
#         edge_travel_time = sorted_times[0][1]
#         while alg_time == edge_travel_time:
#             del sorted_times[0]
#             if vehicle_location not in conflicts:
#                 conflicts[vehicle_location] = [candidate_location]
#             else:
#                 conflicts[vehicle_location].append(candidate_location)
#             if candidate_location not in temporarily_open:
#                 temporarily_open.append(candidate_location)
#             if int(vehicle_location) in unconnected_vehicles:
#                 unconnected_vehicles.remove(int(vehicle_location))
#             if not unconnected_vehicles:
#                 return temporarily_open, conflicts
#             edge_key = sorted_times[0][0]
#             vehicle_location = edge_key.split('-')[0]
#             candidate_location = edge_key.split('-')[1]
#             edge_travel_time = sorted_times[0][1]



def get_conflicts_dict(beta):
    conflicts = dict()
    for vehicle_key in settings.vehicles_locations_over_day:
        for facility_key, vehicles_list in beta.items():
            if beta[facility_key][str(vehicle_key)] > 0:
                if str(vehicle_key) not in conflicts:
                    conflicts[str(vehicle_key)] = [facility_key]
                else:
                    conflicts[str(vehicle_key)].append(facility_key)
    return conflicts


def phase1_weighted(cost, max_alg_time):
    print('\nPhase 1 ...')
    temporarily_open = list()
    tight_edges = list()
    costs = {facility_key: cost for facility_key in list(settings.clusters.keys())}
    beta = {facility_key: {str(vehicle_key): 0 for vehicle_key in settings.vehicles_locations_over_day} for facility_key in list(settings.clusters.keys())}
    sorted_times = sorted(settings.travel_times_over_day.items(), key=lambda kv: kv[1])
    sorted_times = [(key, travel_time) for (key, travel_time) in sorted_times if travel_time != 0]
    unconnected_vehicles = settings.vehicles_locations_over_day[:]

    for alg_time in range(max_alg_time):
        edge_key = sorted_times[0][0]
        edge_travel_time = sorted_times[0][1]

        # Get tight edges
        while alg_time == edge_travel_time:
            if edge_key not in tight_edges:
                tight_edges.append(edge_key)
            del sorted_times[0]
            edge_key = sorted_times[0][0]
            edge_travel_time = sorted_times[0][1]

        # Raise betas
        for tight_edge_key in tight_edges:
            vehicle_key = tight_edge_key.split('-')[0]
            candidate_key = tight_edge_key.split('-')[1]
            beta[candidate_key][vehicle_key] += 1
            if sum(beta[candidate_key].values()) >= costs[candidate_key]:
                temporarily_open.append(candidate_key)
                tight_edges.remove(tight_edge_key)
                for vehicle_key in settings.vehicles_locations_over_day:
                    if beta[candidate_key][str(vehicle_key)] > 0 and int(vehicle_key) in unconnected_vehicles:
                        unconnected_vehicles.remove(int(vehicle_key))
                    if not unconnected_vehicles:
                        conflicts = get_conflicts_dict(beta)
                        return temporarily_open, conflicts


def remove_duplicates(temporarily_open):
    set_of_temporarily_open = list()
    for temporarily_open_facility in temporarily_open:
        if temporarily_open_facility not in set_of_temporarily_open:
            set_of_temporarily_open.append(temporarily_open_facility)
    return set_of_temporarily_open


def get_independent_set(graph, temporarily_open):
    open_facilities = list()
    temporarily_open = remove_duplicates(temporarily_open)
    for temporarily_open_facility in temporarily_open:
        edges_connected = False
        for open_facility in open_facilities:
            if graph.has_edge(temporarily_open_facility, open_facility):
                edges_connected = True
                break
        if not edges_connected:
            open_facilities.append(temporarily_open_facility)
    return open_facilities


def phase2(temporarily_open, conflicts):
    print('\nPhase 2 ...')
    graph = nx.Graph()
    for temporary_facility in temporarily_open:
        graph.add_node(temporary_facility)
        graph.nodes[temporary_facility]['id'] = temporary_facility
    for _, list_of_conflicts in conflicts.items():
        combinations_of_conflicts = combinations(list_of_conflicts, 2)
        for combination in combinations_of_conflicts:
            graph.add_edge(combination[0], combination[1])
    # independent_set = nx.maximal_independent_set(graph)
    independent_set = get_independent_set(graph, temporarily_open)
    return independent_set



def get_opened_facilities_list(cost, max_alg_time):
    temporarily_open, conflicts = phase1_weighted(cost, max_alg_time)
    opened_facilities = phase2(temporarily_open, conflicts)
    return opened_facilities

def get_vehicle_time_to_nearest_location(vehicle_location, locations):
    time_to_nearest_location = float("inf")
    for candidate_location in locations:
        travel_time = settings.travel_times_over_day[str(vehicle_location) + '-' + str(candidate_location)]
        if travel_time < time_to_nearest_location:
            time_to_nearest_location = travel_time
    return time_to_nearest_location


def get_solution_time(opened_facilities):
    total_time = 0
    for vehicle_location in settings.vehicles_locations_over_day:
        total_time += get_vehicle_time_to_nearest_location(vehicle_location, opened_facilities)
    return total_time


def jv_algorithm():
    max_alg_time = max(settings.travel_times_over_day.values())
    min_value = 0
    below_k_solution = []
    max_value = max_alg_time
    med_value = (max_value + min_value) / 2.0
    while max_value - min_value > settings.jv_epsilon:
        print(f'Checking value {med_value} in interval [{min_value}, {max_value}]')
        print(f'max_value - min_value is: {max_value - min_value}')
        opened_facilities = get_opened_facilities_list(med_value, max_alg_time)
        if len(opened_facilities) < settings.k:
            max_value = med_value
            med_value = (max_value + min_value) / 2.0
            below_k_solution = opened_facilities[:]
        elif len(opened_facilities) > settings.k:
            min_value = med_value
            med_value = (max_value + min_value) / 2.0
        else:
            total_travel_time = get_solution_time(opened_facilities)
            return opened_facilities, total_travel_time
        print(f'Number of opened facilities: {len(opened_facilities)} for value {med_value}')
    total_travel_time = get_solution_time(below_k_solution)
    return below_k_solution, total_travel_time
