# YouTube Link: https://www.youtube.com/watch?v=iYJNmuD4McE

# A lock or mutex is a sychronization mechanism for enforcing
# limits on access to a resource in an environment where there
# are many threads of execution.

# More on locks:
# https://en.wikipedia.org/wiki/Lock_(computer_science)

import time
from multiprocessing import Process, Lock, Value
class lockClass:
	def __init__(self, parameters, S, zoneId):
		total = Value('i', 500)
		self.x = {}
		self.omega = {}
		self.st = {}
		self.r = {}
		self.y = {}
		for i in range(5):
			total = Value('i', 500)
			self.x[i] = total
		# for facility in parameters.zonesDict[zoneId].facilities:
		# 	self.omega[facility.id] = S.omega[facility.id]
		# 	self.st[facility.id] = S.st[facility.id]
		# 	self.r[facility.id] = S.r[facility.id]
		# 	self.y[facility.id] = S.y[facility.id]
		# for vehicleKey, _ in parameters.vehiclesDict.items():
		# 	xFacilitiesDict = {}
		# 	for facility in parameters.zonesDict[zoneId].facilities:
		# 		xFacilitiesDict[facility.id] = 0
		# 	self.x[vehicleKey] = xFacilitiesDict

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
	lock = Lock()
	add_proc = Process(target=add_500_lock, args=(total, lock))
	sub_proc = Process(target=sub_500_lock, args=(total, lock))

	add_proc.start()
	sub_proc.start()

	add_proc.join()
	sub_proc.join()
	print(total.value)

