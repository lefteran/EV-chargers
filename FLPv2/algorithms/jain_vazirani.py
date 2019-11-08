# LIBRARIES
from math import floor
import networkx as nx
from tqdm import tqdm
from itertools import combinations
# FILES
import settings



def phase1_unweighted():
    # TODO Check the right value for max_alg_time
    precision = 1000000
    conflicts = dict()
    max_alg_time = 10000000
    temporarily_open = list()
    sorted_times = sorted(settings.travel_times_over_day.items(), key=lambda kv: kv[1])
    sorted_times = [(key, floor(travel_time * precision)) for (key, travel_time) in sorted_times if travel_time != 0]
    unconnected_vehicles = settings.vehicles_locations_over_day[:]

    for alg_time in tqdm(range(max_alg_time)):
        edge_key = sorted_times[0][0]
        vehicle_location = edge_key.split('-')[0]
        candidate_location = edge_key.split('-')[1]
        edge_travel_time = sorted_times[0][1]
        while alg_time == edge_travel_time:
            del sorted_times[0]
            if vehicle_location not in conflicts:
                conflicts[vehicle_location] = [candidate_location]
            else:
                conflicts[vehicle_location].append(candidate_location)
            if candidate_location not in temporarily_open:
                temporarily_open.append(candidate_location)
            if int(vehicle_location) in unconnected_vehicles:
                unconnected_vehicles.remove(int(vehicle_location))
            if not unconnected_vehicles:
                return temporarily_open, conflicts
            edge_key = sorted_times[0][0]
            vehicle_location = edge_key.split('-')[0]
            candidate_location = edge_key.split('-')[1]
            edge_travel_time = sorted_times[0][1]



def phase2(temporarily_open, conflicts):
    print('Phase 2 ...')
    graph = nx.Graph()
    for temporary_facility in temporarily_open:
        graph.add_node(temporary_facility)
        graph.nodes[temporary_facility]['id'] = temporary_facility
    for _, list_of_conflicts in tqdm(conflicts.items()):
        combinations_of_conflicts = combinations(list_of_conflicts, 2)
        for combination in combinations_of_conflicts:
            graph.add_edge(combination[0], combination[1])
    independent_set = nx.maximal_independent_set(graph)
    return independent_set


def phase3(opened_facilities):
    a=2
    # TODO lagrangian relaxation
    #  do binary search in the interval of costs [0, n*c_max],
    #  where c_max is the length of longest edge check JV p.285


def jv_algorithm():
    temporarily_open, conflicts = phase1_unweighted()
    opened_facilities = phase2(temporarily_open,conflicts)
    phase3(opened_facilities)
    return temporarily_open