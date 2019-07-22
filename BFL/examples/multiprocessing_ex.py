# YouTube Link: https://www.youtube.com/watch?v=RR4SoktDQAw

# Introduction an simple example of the multiprocessing module in Python.
# We show how to simply apply this module to a function that takes a number
# and squares it.

import os
import time
from math import sqrt
from multiprocessing import Process, Lock, Value


def calculate(lowerNumber, upperNumber):
    [sqrt(i ** 2) for i in range(lowerNumber, upperNumber)]
    proc_id = os.getpid()
    print(f"Process ID: {proc_id}")

    # process_name = current_process().name
    # print(f"Process Name: {process_name}")


def multiprocessingMethod():
    start_time = time.time()
    processes = []
    numbers = [0, 25000000, 50000000, 75000000]
    difference = 25000000

    for i, lowerNumber in enumerate(numbers):
        upperNumber = lowerNumber + difference
        process = Process(target=calculate, args=(lowerNumber, upperNumber))
        processes.append(process)

        process.start()

    for process in processes:
        process.join()
    print("--- %s seconds ---" % (time.time() - start_time))


def singleprocessingMethod():
    start_time = time.time()
    lowerNumber = 0
    upperNumber = 100000000
    calculate(lowerNumber, upperNumber)
    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == '__main__':
    # singleprocessingMethod()
    multiprocessingMethod()