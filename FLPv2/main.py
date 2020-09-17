# LIBRARIES
import time
# FILES
import settings
# sys.path.append('project folder path')

# import network.run as network
import algorithms.run as algorithms
# import visualisation.run as visualisation

# import network.slice_paths_from_delos as slice_paths
# import scripts.compute_rho_list as rho_list
# import scripts.counts_from_json_files as json_counts
# import scripts.edit_building_permits as permits
import scripts.customer_demand_and_network_analytics as customer_demand


if __name__ == "__main__":
    settings.start_time = time.time()

    # NETWORK
    # network.run()

    # ALGORITHMS
    algorithms.run()

    # SCRIPTS
    # create_dat_for_optimal.create_dat_file()
    # import_vehicles_paths_from_delos.export_charging_spots_per_hour_dict_and_statistics()
    # data_export_for_visualisation.export_solution_locations_coordinates()
    # rm_timestamps.remove_timestamps()
    # existing_stations_csv_to_json.export_csv_to_json()
    # charging_demand.compute_traffic_demand()
    # analytics.get_analytics()
    # rho_list.compute_rho_list()
    # json_counts.count_idle_vehicles()
    # permits.building_permits_to_json()
    # customer_demand.edit_customer_demand_file()
    # customer_demand.clear_resample_and_reorder_demand()

    # POST OPTIMIZATION
    # charging_points.get_number_of_charging_points_per_station()

    # VISUALISATION
    # visualisation.run()

    print("--- %s seconds ---" % (time.time() - settings.start_time))

