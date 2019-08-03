# LIBRARIES
import time
# FILES
# import scenarios.run as scenarios
import algorithms.run as algorithms


if __name__ == "__main__":
    start_time = time.time()

    # scenarios.run()
    algorithms.run()

    print("--- %s seconds ---" % (time.time() - start_time))