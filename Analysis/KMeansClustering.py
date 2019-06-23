import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, StandardScaler
from Tools.Utils import Utils
import logging


class KMeansClustering:

    def __init__(self, type_of_initialisation, features, blocks, fixed):
        self.type_of_initialization = type_of_initialisation
        self.features = features
        self.blocks = blocks
        self.fixed = fixed
        self.dict_clusters = {}

    def __get_cluster_heuristic(self, n_clusters, X, list_of_initial_centroids):
        """ Method to find obtain a KMeans object with initial centroids
        chosen based on a given heuristic.
        :param n_clusters: number of clusters
        :type n_clusters: int
        :param X: the feature array
        :type X: numpy array
        :param list_of_initial_centroids: list with initial centroids based on number of clusters
        :type list_of_initial_centroids: list of lists
        """
        initial_positions = []
        logging.info("Heuristic initialization based on {}".format(self.type_of_initialization))
        Utils.get_centroids_heuristic(n_clusters, self.features, initial_positions, self.type_of_initialization)
        initial_centroids = [X[index] for index in initial_positions]
        list_of_initial_centroids.append(initial_centroids)
        clusterer = KMeans(n_clusters=n_clusters, init=np.array(initial_centroids), random_state=10)
        return clusterer

    def __compute_for_fixed_clusters(self, X, list_of_initial_centroids):
        logging.info("Starting with fix number of clusters")
        if 'RANDOM' not in self.type_of_initialization:
            self.__get_cluster_heuristic(self.fixed, X, list_of_initial_centroids)
            self.__compute_clustering(self.fixed, list_of_initial_centroids[0])
        else:
            logging.info("Random initialisation")
            self.__compute_clustering(self.fixed)

    def __find_best_clustering(self):

        """ Method to find the best number of clusters in a range from 2 to 6"""

        logging.info("Starting K-Means Algorithm")
        min_max_scaler = MinMaxScaler()
        X_train_norm = min_max_scaler.fit_transform(np.array(self.features))
        X = np.array(X_train_norm)
        silhouette_list = []
        initial_centroids = None
        list_of_initial_centroids = []
        if self.fixed:
            self.__compute_for_fixed_clusters(X, list_of_initial_centroids)
        else:
            for n_clusters in range(2, 6):
                if 'RANDOM' not in self.type_of_initialization:
                    clusterer = self.__get_cluster_heuristic(n_clusters, X, list_of_initial_centroids)
                else:
                    logging.info("Random initialisation")
                    clusterer = KMeans(n_clusters=n_clusters, random_state=10, n_init=10)

                cluster_labels = clusterer.fit_predict(X)
                silhouette_avg = silhouette_score(X, cluster_labels)
                silhouette_list.append(silhouette_avg)
                logging.info("For {}".format(n_clusters) +
                         " clusters, the average silhouette_score is : {}".format(silhouette_avg))

            number_of_clusters = silhouette_list.index(max(silhouette_list)) + 2

            if initial_centroids:
                initial_centroids = list_of_initial_centroids[number_of_clusters-2]

            logging.info("The best number of clusters is {}".format(number_of_clusters))
            self.__compute_clustering(number_of_clusters, initial_centroids)

    def __compute_clustering(self, num_clusters, initial_centroids=None):
        """ Method to compute clustering after the best number of clusters had been found
        :param num_clusters: number of clusters found for the best partitions
        :type num_clusters: int
        :param initial_centroids: the initial centroids
        :type initial_centroids: None for random initialization or list
        """

        min_max_scaler = MinMaxScaler()
        X_train_norm = min_max_scaler.fit_transform(self.features)
        X = np.array(X_train_norm)
        if initial_centroids:
            clusterer = KMeans(n_clusters=num_clusters, init=np.array(initial_centroids), random_state=10)
        else:
            clusterer = KMeans(n_clusters=num_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(X)
        return self.__return_as_dict(cluster_labels, num_clusters)

    def __return_as_dict(self, clusters_labels, num_clusters):
        """ Method to form a dictionary for the resulting partitions
        with the following structure
        key: cluster_number
        value: list of blocks within the given cluster
        :param clusters_labels: the labels of clusters
        :type clusters_labels: list of integers
        :param num_clusters: the number of clusters
        :type num_clusters: integer"""

        for i in range(0, num_clusters):
            cluster_blocks = [block for (label, block) in zip(clusters_labels, self.blocks) if label == i]
            self.dict_clusters[i] = cluster_blocks

        return self.dict_clusters

    def compute(self):
        return self.__find_best_clustering()
