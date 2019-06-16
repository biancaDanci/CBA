import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from Utils import Utils

class KMeansClustering:

    def __init__(self, type_of_initialisation, features, blocks):
        self.type_of_initialization = type_of_initialisation
        self.features = features
        self.blocks = blocks
        self.dict_clusters = {}

    def find_best_clustering(self):

        """ Method to find the best number of clusters in a range from 2 to 6"""

        min_max_scaler = MinMaxScaler()
        X_train_norm = min_max_scaler.fit_transform(np.array(self.features))
        X = np.array(X_train_norm)
        silhouette_list = []
        initial_centroids = None
        for n_clusters in range(2, 5):
            if self.type_of_initialization == 'HEURISTIC':
                initial_positions = []
                Utils.get_centroids_text_denisity(n_clusters, self.features, initial_positions)
                initial_centroids = [X[index] for index in initial_positions]
                clusterer = KMeans(n_clusters=n_clusters, init=np.array(initial_centroids), random_state=10)
            else:
                clusterer = KMeans(n_clusters=n_clusters, random_state=10)
            cluster_labels = clusterer.fit_predict(X)
            silhouette_avg = silhouette_score(X, cluster_labels)
            silhouette_list.append(silhouette_avg)
            print("For n_clusters =", n_clusters,
                  "The average silhouette_score is :", silhouette_avg)

        number_of_clusters = silhouette_list.index(max(silhouette_list)) + 2
        number_of_clusters = 4
        print("The best number of clusters is {}".format(number_of_clusters))
        self.compute_clustering(number_of_clusters, initial_centroids)

    def compute_clustering(self, num_clusters, initial_centroids=None):
        min_max_scaler = MinMaxScaler()
        X_train_norm = min_max_scaler.fit_transform(self.features)
        X = np.array(X_train_norm)
        if initial_centroids:
            clusterer = KMeans(n_clusters=num_clusters,init=np.array(initial_centroids), random_state=10)
        else:
            clusterer = KMeans(n_clusters=num_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(X)
        print('done compute clustering')
        return self.return_as_dict(cluster_labels, num_clusters)

    def return_as_dict(self, clusters_labels, num_clusters):
        """Method to form a dictionary for the resulting partitions
        with the following structure
        key: cluster_number
        value: list of blocks within the given cluster"""
        
        for i in range(0, num_clusters):
            cluster_blocks = [block for (label, block) in zip(clusters_labels, self.blocks) if label == i]
            self.dict_clusters[i] = cluster_blocks
        print('in k means' + str(self.dict_clusters.keys()))
        return self.dict_clusters

    def computeKM(self):
        return self.find_best_clustering()
