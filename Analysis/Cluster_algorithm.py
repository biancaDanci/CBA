from KMeansClustering import KMeansClustering
from XMeansClustering import XMeansClustering


class Cluster:

    def __init__(self, algorithm, type_of_initialization, features, blocks):
        self.algorithm = algorithm
        self.type_of_initialization = type_of_initialization
        self.features = features
        self.blocks = blocks

    def compute(self):
        if self.algorithm == 'K-Means':
            cl_algorithm = KMeansClustering(self.type_of_initialization, features=self.features, blocks=self.blocks)

            cl_algorithm.computeKM()
            print('Clusters'+str(cl_algorithm.dict_clusters.keys()))
            return cl_algorithm.dict_clusters
        else:
            cl_algorithm = XMeansClustering(self.type_of_initialization, features=self.features, blocks=self.blocks)

            cl_algorithm.computeXM()
            print('Clusters'+str(cl_algorithm.dict_clusters.keys()))
            return cl_algorithm.dict_clusters



