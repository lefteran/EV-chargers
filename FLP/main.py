# LIBRARIES
import time
# FILES
# import scenarios.run as scenarios
import algorithms.run as algorithms
import scripts.createDataForOptimal as createDataForOptimal


if __name__ == "__main__":
    start_time = time.time()

    # SCRIPTS



    # ALGORITHMS
    # scenarios.run()
    algorithms.run()

    # createDataForOptimal.convertCsvToDat()
    print("--- %s seconds ---" % (time.time() - start_time))