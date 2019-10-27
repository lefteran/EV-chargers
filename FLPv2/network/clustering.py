# LIBRARIES
import pandas as pd
import json
# FILES
import settings


def get_clusters(nodes):
	from sklearn.cluster import KMeans
	from sklearn.metrics import pairwise_distances_argmin_min

	nodes_coordinates_list = list()
	nodes_ids = list()
	cluster_labeling = dict()
	clusters = dict()
	for node_key, node_value in nodes.items():
		nodes_coordinates_list.append((node_value['y'], node_value['x']))
		nodes_ids.append(node_value['id'])
	df = pd.DataFrame(nodes_coordinates_list, columns=['y', 'x'])
	kmeans = KMeans(n_clusters=settings.centroids).fit(df)
	node_clustering_labels = kmeans.labels_
	centroids = kmeans.cluster_centers_
	closest_node_list_indices_to_centroids, _ = pairwise_distances_argmin_min(centroids, nodes_coordinates_list)
	for index, node_id in enumerate(closest_node_list_indices_to_centroids):
		cluster_labeling[index] = nodes_ids[node_id]
	for index, node_label in enumerate(node_clustering_labels):
		if cluster_labeling[node_label] not in clusters:
			clusters[cluster_labeling[node_label]] = list()
		clusters[cluster_labeling[node_label]].append(nodes_ids[index])
	return clusters


def save_clusters(dict_to_be_saved):
	filename = settings.cluster
	json_file = json.dumps(dict_to_be_saved)
	f = open(filename, 'w')
	f.write(json_file)
	f.close()


def load_clusters():
	filename = settings.cluster
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict