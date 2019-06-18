import numpy as np
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from Tools.Utils import Utils
from pyclustering.cluster.xmeans import xmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
import logging


class XMeansClustering:
    """Class for clustering based on X-Means algorithm"""
    def __init__(self, type_of_initialisation, features, blocks):
        self.type_of_initialization = type_of_initialisation
        self.features = features
        self.blocks = blocks
        self.dict_clusters = {}

    def __get_centroids_heuristic(self, n_clusters, X):
        """ Method to find obtain initial centroids
        chosen based on a given heuristic.
        :param n_clusters: number of clusters
        :type n_clusters: int
        :param X: the feature array
        :type X: numpy array
        """
        initial_positions = []
        logging.info("Heuristic initialization based on {}".format(self.type_of_initialization))
        Utils.get_centroids_heuristic(n_clusters, self.features, initial_positions, self.type_of_initialization)
        initial_centroids = [X[index] for index in initial_positions]
        return initial_centroids

    def __compute(self):
        """Method to find the best partitions using X-Means"""
        min_max_scaler = MinMaxScaler()
        X_train_norm = min_max_scaler.fit_transform(np.array(self.features))
        X = np.array(X_train_norm)

        amount_initial_centers = 2
        if 'RANDOM' not in self.type_of_initialization:
            initial_centers = self.__get_centroids_heuristic(amount_initial_centers, X)

        else:
            logging.info("Random initialization")
            initial_centers = kmeans_plusplus_initializer(X, amount_initial_centers).initialize()

        xmeans_instance = xmeans(X, initial_centers, 5)
        xmeans_instance.process()

        clusters = xmeans_instance.get_clusters()
        centers = xmeans_instance.get_centers()
        i = 0
        for elem in clusters:
            if isinstance(elem, list):
                aux = []
                for el in elem:
                    aux.append(self.blocks[int(el)])
            self.dict_clusters[i] = aux
            i = i + 1
        logging.info("X-Means found {} clusters".format(str(len(clusters))))
        return self.dict_clusters

    def compute(self):
        return self.__compute()
