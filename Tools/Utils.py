import logging


class Utils:
    """Class used to compute the initial centroids using a given criteria"""

    @staticmethod
    def sortByTextDensity(obj):
        return obj[0][4]

    @staticmethod
    def sortByFontSize(obj):
        return obj[0][0]

    @staticmethod
    def sortByDimension(obj):
        return obj[0][1]+obj[0][2]

    @staticmethod
    def sortBySentenceLength(obj):
        return obj[0][3]

    @staticmethod
    def find_method_and_sort_by(features_with_positions, sort_by):
        """Method for choosing the function to sort the features with
        and returns the sorted array of features.
        :param features_with_positions: tuple of position array and features array
        :param features_with_positions: tuple
        :param sort_by: string defining the function to sort the array with
        :param sort_by: string
        """

        logging.info("Choosing the type of initialization")

        if sort_by == 'FONT SIZE':
            features_ordered = sorted(features_with_positions, key=Utils.sortByFontSize)
        elif sort_by == 'DIMENSION':
            features_ordered = sorted(features_with_positions, key=Utils.sortByDimension)
        elif sort_by == 'TEXT DENSITY':
            features_ordered = sorted(features_with_positions, key=Utils.sortByTextDensity)
        else:
            features_ordered = sorted(features_with_positions, key=Utils.sortBySentenceLength)
        return features_ordered

    @staticmethod
    def get_centroids_heuristic(number_of_clusters, features, results, sort_by):
        """Method to return the positions of the best initial centroids
        using a given string representing the sorting criteria.
        :param number_of_clusters: the number of clusters, equal to the number of desired centroids
        :type number_of_clusters: int
        :param features: the array representing the features extracted
        :type features: array
        :param results: empty list to store the results in
        :type results: list
        :param sort_by: string
        """

        positions = [i for i in range(0, len(features))]
        features_with_position = zip(features, positions)

        features_ordered = Utils.find_method_and_sort_by(features_with_position, sort_by)
        number = len(features_ordered) / number_of_clusters

        for i in range(0, number_of_clusters):
            if i == 0:
                results.append(features_ordered[(len(features_with_position) - 1 - number * i)][1])
            else:
                results.append(features_ordered[(len(features_with_position) - number * i)][1])
        logging.info("The best centers have been found based on {}".format(sort_by))
