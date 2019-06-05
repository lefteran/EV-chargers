import matplotlib.pyplot as plt

filename='TransportationNetworks/SiouxFalls/SiouxFalls_node.tntp'
fp=open(filename,"r")
xcoords=[]
ycoords=[]
next(fp)
for line in fp:
	elements=line.split("\t")
	x=float(elements[1])
	y=float(elements[2])
	xcoords.append(x/10000)
	ycoords.append(y/10000)
fp.close()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(xcoords, ycoords, color='darkgreen', marker='o')
plt.show()