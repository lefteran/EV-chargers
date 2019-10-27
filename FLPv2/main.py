# LIBRARIES
import time
# FILES
import network.run as network
# import algorithms.run as algorithms
import settings
# import visualisation.run as visualisation
# import scripts.createDataForOptimal as createDataForOptimal


if __name__ == "__main__":
    settings.start_time = time.time()

    # NETWORK
    network.run()


    # SCRIPTS
    # createDataForOptimal.convertCsvToDat()

    # ALGORITHMS
    # algorithms.run()

    # VISUALISATION
    # visualisation.run()

    print("--- %s seconds ---" % (time.time() - settings.start_time))

