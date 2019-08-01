# LIBRARIES
import time
# FILES
import settings
import algorithms.run as algorithms


if __name__ == "__main__":
    start_time = time.time()

    settings.init()
    algorithms.run()

    print("--- %s seconds ---" % (time.time() - start_time))