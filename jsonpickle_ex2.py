from typing import Dict
import jsonpickle
import json

class Solution:
	omega: Dict[str, int]

	def __init__(self):
		self.x = {}
		self.y = {'1': 1, '2': 2, '3': 3}
		self.omega = {'4': 4, '5': 5, '6': 6}
		self.x['a'] = self.omega
		self.x['b'] = self.omega


# obj = Solution()
# serializedObj = jsonpickle.encode(obj)
# with open('solutionJsonPickleTest.json', 'w') as f:
# 	json.dump(serializedObj, f)

with open('solutionJsonPickleTest.json') as json_file:
	importedData = json.load(json_file)
	readObj = jsonpickle.decode(importedData)
	a=2