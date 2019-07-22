# YouTube Link: https://www.youtube.com/watch?v=iYJNmuD4McE

# A lock or mutex is a sychronization mechanism for enforcing
# limits on access to a resource in an environment where there
# are many threads of execution.

# More on locks:
# https://en.wikipedia.org/wiki/Lock_(computer_science)

import time
from multiprocessing import Process, Lock, Value
class lockClass:
	def __init__(self):
		self.x = {}
		self.omega = {}
		self.st = {}
		self.r = {}
		self.y = {}
		for i in range(5):
			self.x[i] = Value('i', i*500)

def add_500_lock(total, lock):
	for i in range(100):
		time.sleep(0.01)
		lock.acquire()
		total.value += 5
		lock.release()


def sub_500_lock(total, lock):
	for i in range(100):
		time.sleep(0.01)
		lock.acquire()
		total.value -= 5
		lock.release()


if __name__ == '__main__':

	total = Value('i', 500)
	sol = lockClass()
	lock = Lock()
	add_proc = Process(target=add_500_lock, args=(total, lock))
	sub_proc = Process(target=sub_500_lock, args=(total, lock))

	add_proc.start()
	sub_proc.start()

	add_proc.join()
	sub_proc.join()
	print(total.value)

