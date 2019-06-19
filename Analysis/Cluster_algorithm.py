from KMeansClustering import KMeansClustering
from XMeansClustering import XMeansClustering
import logging


class Clustering:

    """Class used for initializing the clusterer based on given types"""

    def __init__(self, algorithm, type_of_initialization, features, blocks, fixed):
        self.algorithm = algorithm
        self.type_of_initialization = type_of_initialization
        self.features = features
        self.blocks = blocks
        self.fixed = fixed

    def compute(self):
        """Method used to initialize a type of clustering based on some given types"""

        if self.algorithm == 'K-Means':
            cl_algorithm = KMeansClustering(self.type_of_initialization, features=self.features, blocks=self.blocks, fixed=self.fixed)
        else:
            cl_algorithm = XMeansClustering(self.type_of_initialization, features=self.features, blocks=self.blocks)

        cl_algorithm.compute()
        logging.info('Clusters keys are'+str(cl_algorithm.dict_clusters.keys()))
        return cl_algorithm.dict_clusters



