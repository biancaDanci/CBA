import numpy as np
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from Utils import Utils
from pyclustering.cluster.xmeans import xmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer


class XMeansClustering:
    def __init__(self, type_of_initialisation, features, blocks):
        self.type_of_initialization = type_of_initialisation
        self.features = features
        self.blocks = blocks
        self.dict_clusters = {}

    def compute(self):

        min_max_scaler = MinMaxScaler()

        X_train_norm = min_max_scaler.fit_transform(np.array(self.features))
        X = np.array(X_train_norm)

        amount_initial_centers = 4
        if 'HEURISTIC' in self.type_of_initialization:
            initial_positions = []
            if 'CSS' in self.type_of_initialization:
                print("ii ok am prins heuristic css")
                Utils.get_centroids_font(amount_initial_centers, self.features, initial_positions)
            else:
                Utils.get_centroids_text_denisity(amount_initial_centers, self.features, initial_positions)
            initial_centers = [X[index] for index in initial_positions]

        else:
            initial_centers = kmeans_plusplus_initializer(X, amount_initial_centers).initialize()

        xmeans_instance = xmeans(X, initial_centers, 5)
        xmeans_instance.process()

        clusters = xmeans_instance.get_clusters()
        i = 0
        for elem in clusters:
            if isinstance(elem, list):
                aux = []
                for el in elem:
                    aux.append(self.blocks[int(el)])
            self.dict_clusters[i] = aux
            i = i + 1
        print("Am gasit atati clusteri"+str(len(clusters)))
        print(self.dict_clusters)

        return self.dict_clusters

    def computeXM(self):
        return self.compute()
