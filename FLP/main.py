# LIBRARIES
import time
# FILES
import algorithms.run as algorithms
import scripts.createDataForOptimal as createDataForOptimal


if __name__ == "__main__":
    start_time = time.time()

    # SCRIPTS
    # createDataForOptimal.convertCsvToDat()

    # ALGORITHMS
    algorithms.run()

    print("--- %s seconds ---" % (time.time() - start_time))