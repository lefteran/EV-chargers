# facilities
n=2
# zones
m=2

s=[0 for i in range(n)]
f=[0 for i in range(n)]
r=[0 for i in range(n)]
y=[0 for i in range(n)]

#########
# DATA
#########
a=[1,0]

B=[[0,1], [1,0]]

A=[[1,1], [1,1]]

cs=[3, 2]
cf=[6, 5]
cr=[24, 15]

dem=[30,5]

Nz=[20,26]

cap=[8,14]

R=11

gamma=0.5

#########


cr_sorted_indices = sorted(range(len(cr)),key=cr.__getitem__)
cs_sorted_indices = sorted(range(len(cs)),key=cs.__getitem__)


print("cr_sorted_indices is: ", cr_sorted_indices)

# cs.sort()
# cr.sort()

for z in range(m):
	for i in cr_sorted_indices:
		onstreet = 0
		for k in range(n):
			onstreet = onstreet + a[k] * B[k][z] * y[k]
		while B[i][z] == 1 and sum(r) < R and onstreet < Nz[z] and y[i] < cap[i]:
			r[i] = r[i]+1
			y[i] = y[i]+1
			onstreet = 0
			for k in range(n):
				onstreet = onstreet + a[k] * B[k][z] * y[k]


for z in range(m):
	for i in cs_sorted_indices:
		onstreet = 0
		for k in range(n):
			onstreet = onstreet + a[k] * B[k][z] * y[k]

		supply = 0
		for j in range(m):
			value = 0
			for l in range(n):
				value = value + B[l][j] * y[l]
			supply = supply + A[z][j] * value


		while B[i][z] == 1 and onstreet < Nz[z] and y[i] < cap[i] and supply < (gamma * dem[z]) :
			s[i] = s[i] + 1
			y[i] = y[i] + 1
			onstreet = 0
			for l in range(n):
				onstreet = onstreet + a[l] * B[l][z] * y[l]


objective = 0
for i in range(n):
	objective = objective + cs[i] * s[i] + cr[i] * r[i]

print("\nObjective is: ", objective)


print("Slow chargers are: ")
print(s)
print("Rapid chargers are: ")
print(r)
print("All chargers are: ")
print(y)