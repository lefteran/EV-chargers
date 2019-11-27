import _pickle as pickle


class dictionaryMapping(dict):

    def getValue(self, vehicle):
        return self.__dict__[vehicle]

    def getSubValue(self, vehicle, facility):
        return self.__dict__[vehicle][facility]

    def copy(self):
        return self.__dict__.copy()

    def setDict(self, oldDict):
        self.__dict__ = pickle.loads(pickle.dumps(oldDict, -1))




myDict = {'1': 1, '2': 2, '3': 3}
subDict = {}
subDict['a'] = 'b'
subDict['c'] = 'd'
myDict['4'] = subDict
newDict = dictionaryMapping()
newDict.setDict(myDict)
a= newDict.getValue('1')
b= newDict.getSubValue('4', 'c')
print(f"a is {a} and b is {b}")