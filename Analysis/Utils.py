class Utils:

    @staticmethod
    def sortByTextDensity(obj):
        return obj[0][4]

    @staticmethod
    def get_centroids_text_denisity(number_of_clusters, features, results):

        positions = [i for i in range(0, len(features))]
        features_with_position = zip(features, positions)
        features_ordered = sorted(features_with_position, key=Utils.sortByTextDensity)

        number = len(features_ordered)/number_of_clusters

        for i in range(0, number_of_clusters):
            if i == 0:
                results.append(features_ordered[(len(features_with_position)-1-number*i)][1])
            else:
                results.append(features_ordered[(len(features_with_position)-number*i)][1])
