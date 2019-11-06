# LIBRARIES
import time
# FILES
# import network.run as network
import scripts.create_dat_for_optimal as create_dat_for_optimal
import algorithms.run as algorithms
import settings
# import visualisation.run as visualisation
import scripts.import_vehicles_paths_from_delos as import_vehicles_paths_from_delos


if __name__ == "__main__":
    settings.start_time = time.time()

    # NETWORK
    # network.run()


    # SCRIPTS
    # create_dat_for_optimal.create_dat_file()
    # import_vehicles_paths_from_delos.export_charging_spots_per_hour_dict_and_statistics()


    # ALGORITHMS
    algorithms.run()

    # VISUALISATION
    # visualisation.run()

    print("--- %s seconds ---" % (time.time() - settings.start_time))

