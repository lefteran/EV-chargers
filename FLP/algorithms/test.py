



data = [('145646',15), ('46757',9), ('75734',89)]

print(f"data is {data}")
data.sort(key=lambda tup: tup[1])
print(f"sorted data are {data}")

myDict = dict(data)
print(f"element is {myDict['145646']}")
