from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

Data = {'x': [25,34,22,27,33,33,31,22,35,34,67,54,57,43,50,57,59,52,65,47,49,48,35,33,44,45,38,43,51,46],
        'y': [79,51,53,78,59,74,73,57,69,75,51,32,40,47,53,36,35,58,59,50,25,20,14,12,20,5,29,27,8,7]
       }

df = DataFrame(Data,columns=['x','y'])

kmeans = KMeans(n_clusters=1).fit(df)
centroids = kmeans.cluster_centers_
# arr = np.array([Data[key] for key in Data.keys()])
closest, _ = pairwise_distances_argmin_min(centroids, [[25,79], [34,51]])
print(centroids)
print(closest)
