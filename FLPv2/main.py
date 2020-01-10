# LIBRARIES
import time
# FILES
import settings
# sys.path.append('project folder path')
import network.run as network
import scripts.data_export_for_visualisation as data_export_for_visualisation
import scripts.create_dat_for_optimal as create_dat_for_optimal
import scripts.get_charging_points as charging_points
import scripts.remove_timestamps as rm_timestamps
import scripts.existing_stations_csv_to_json as existing_stations_csv_to_json
import scripts.charging_demand as charging_demand
# import algorithms.run as algorithms
# import visualisation.run as visualisation
import scripts.import_vehicles_paths_from_delos as import_vehicles_paths_from_delos


if __name__ == "__main__":
    settings.start_time = time.time()

    # NETWORK
    # network.run()


    # SCRIPTS
    # create_dat_for_optimal.create_dat_file()
    # import_vehicles_paths_from_delos.export_charging_spots_per_hour_dict_and_statistics()
    # data_export_for_visualisation.export_solution_locations_coordinates()
    # rm_timestamps.remove_timestamps()
    # existing_stations_csv_to_json.export_csv_to_json()
    charging_demand.compute_demand()

    # ALGORITHMS
    # algorithms.run()


    # POST OPTIMIZATION
    # charging_points.get_number_of_charging_points_per_station()

    # VISUALISATION
    # visualisation.run()

    print("--- %s seconds ---" % (time.time() - settings.start_time))

