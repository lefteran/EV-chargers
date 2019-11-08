mylist = [('a', 1), ('b', 1), ('b', 2), ('a', 2), ('c', 15)]
print(f'my list is {mylist}')
mylist = [(x,y) for (x,y) in mylist if y!=2]
print(f'new list is {mylist}')