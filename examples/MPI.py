import time
from math import sqrt
from mpi4py import MPI

start_time = time.time()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# ########## 1 PROCESS #####################
# [sqrt(i ** 2) for i in range(100000000)]
# print("hello from process ", rank)
# print("size is ", comm.Get_size())

# ########### MULTIPROCESSING #################
if rank == 0:
    [sqrt(i ** 2) for i in range(0,25000000)]
if rank == 1:
    [sqrt(i ** 2) for i in range(25000000, 50000000)]
if rank == 2:
    [sqrt(i ** 2) for i in range(50000000, 75000000)]
if rank == 3:
    [sqrt(i ** 2) for i in range(75000000, 100000000)]

print("--- %s seconds ---" % (time.time() - start_time))