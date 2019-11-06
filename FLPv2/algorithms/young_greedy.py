# LIBRARIES
# FILES
import settings


def get_objective_value_of_fractional_solution():
    objective_value = 0

    return objective_value


def young_greedy():
    T_f = get_objective_value_of_fractional_solution()
    ell = dict()
    phi = dict()

    for vehicle_location in settings.vehicles_locations_over_day:
        ell[vehicle_location] = None

    # for location in settings.clusters.keys():

# dict for l_i