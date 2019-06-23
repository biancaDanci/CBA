import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import logging

PATH = '/home/bia/PycharmProjects/CBA/Outputs/stats/'


class Statistics:
    """Class for displaying results and features in a statistics manner."""
    def __init__(self, clusters, features):
        self.features = features
        self.clusters = clusters
        self.name_features_text = ['Number_of_words', 'Quotient_number_of_words', 'Sentence_length',
                                   'Quotient_sentence_length', 'Text_density', 'Quotient_text_density',
                                   'Link density']
        self.name_features_visual = ['FONT SIZE', 'HEIGHT', 'WIDTH', 'BACKGROUND COLOR', 'BORDER COLOR',
                                     'TEXT COLOR', 'FONT STYLE']

    def __show_each_feature(self, feature_name, feature_number):
        """Method to display the way a feature vary regarding its position
        in the retrieved elements.
        :param feature_name: the name of the analyzed feature
        :type feature_name: string
        :param feature_number: the position of the feature in the feature array
        :type feature_number: int"""
        if feature_name=="Text_density":
            from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, StandardScaler
            min_max_scaler = MinMaxScaler()
            X_train_norm = min_max_scaler.fit_transform(self.features)
            X = np.array(X_train_norm)
            y = np.array([feature[feature_number] for feature in X])
            sns.set()
            plt.title(feature_name)
            plt.xlabel('Position')
            plt.ylabel('Value')
            plt.plot(y[:], 'bo', y, 'k')
            path = PATH + feature_name+'.jpg'
            plt.savefig(path)

    def __show_all_features_individually(self, features_type):
        """Method to display in a statistical manner
        the way features vary in the web page.
        :param features_type: the name of features to display TEXT or VISUAL
        :type features_type: string
        """
        position = 0
        logging.info("Showing {} feature".format(features_type))
        if features_type == 'TEXT':
            features_names = self.name_features_text
        else:
            features_names = self.name_features_visual

        for feature_name in features_names:
            self.__show_each_feature(feature_name, position)
            position += 1

    def __show_all_features(self, features_types):
        """Method to show the feature joint relationships.
        :param features_types: the type of features to display
        :type features_types: str"""
        logging.info("Showing all {} features".format(features_types))
        if features_types == "TEXT":
            data_to_display = self.name_features_text
        else:
            data_to_display = self.name_features_visual

        data = pd.DataFrame(self.features, columns=data_to_display)
        sns.set()
        sns.pairplot(data)
        path = PATH + 'features_relationship.jpg'
        plt.savefig(path)

    def __show_results_clustering(self, features_types, blocks):
        """"Method to show the feature joint relationships
        based on the cluster they belong to.
        :param features_types: the type of features to display
        :type features_types: str
        :param blocks: the WebElements retrieved
        :type blocks: list of WebElements"""
        logging.info("Showing all {} features colored by cluster".format(features_types))
        if features_types == "TEXT":
            data_to_display = self.name_features_text
        else:
            data_to_display = self.name_features_visual
        to_display = []
        for element_position in range(0, len(blocks)):
            for key in self.clusters.keys():
                if blocks[element_position] in self.clusters[key]:
                    features = self.features[element_position]
                    features.append('Cluster {}'.format(key))
                    to_display.append(features)
        data_to_display.append('Cluster')
        data = pd.DataFrame(to_display, columns=data_to_display)
        sns.set()
        sns.pairplot(data, hue="Cluster")
        path = PATH + 'feature_cluster_distribution.jpg'
        plt.savefig(path)

    def show_statistics(self, features_types, blocks):
        """Method to show the features statistically.
        :param features_types: the type of features to display
        :type features_types: str
        :param blocks: the WebElements retrieved
        :type blocks: list of WebElements"""
        #self.__show_results_clustering(features_types, blocks)
        #self.__show_all_features(features_types)
        #self.__show_all_features_individually(features_types)




