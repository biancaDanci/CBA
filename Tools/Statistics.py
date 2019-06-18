import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import seaborn as sns
import pandas as pd


class Statistics:
    """Class for displaying results and features in a statistics manner."""
    def __init__(self, clusters, features):
        self.features = features
        self.clusters = clusters
        self.name_features_text = ['Number of words', 'Quotient number of words', 'Sentence length',
                                   'Quotient sentence length', 'Text density', 'Quotient text density',
                                   'Link density']
        self.name_features_visual = ['FONT SIZE', 'HEIGHT', 'WIDTH', 'BACKGROUND COLOR', 'BORDER COLOR',
                                     'TEXT COLOR', 'FONT STYLE']


    def show_features_before_clustering(self):
        sns.set()

        data_i = [[bla, text_denisity, word_no, 'bla'] for [bla, text_denisity, word_no] in
               zip([x[2] for x in self.features], [x[1] for x in self.features],[x[0] for x in self.features])]
        #[i for i in range(0, len(self.features))]
  #      plt.plot([position[0] for position in data], [text[1] for text in data])
 #       plt.legend('ABCDEF', ncol=2, loc='upper left');
#        plt.show()

        data_s = [[1,2], [2,3], [3, 7], [4, 11]]
        for i in range(0, len(data_i)):
            if i%2 == 0:
                data_i[i][3]='altceva'

        data = pd.DataFrame(data_i, columns=[
           'number', 'value', 'denisty', 'c'
        ])

        #data['number'].hist(bins=1)


        plt.ylabel("Frequency", fontsize=15)


        for col in ['number', 'value', 'denisty']:
            sns.kdeplot(data[col], shade=True)
        sns.pairplot(data, hue="c")
        plt.show()
        # g = sns.PairGrid(data)
        # g.map_diag(sns.kdeplot)
        # g.map_offdiag(sns.kdeplot, n_levels=6, hue='c')
        # #plt.show()
        #
        # sns.pairplot(data, hue='c', diag_kind='kde',
        #              plot_kws={'alpha': 0.6, 's': 80, 'edgecolor': 'k'},
        #              height=4)
        plt.show()

    def __show_each_feature(self, feature_name, feature_number):
        """Method to display the way a feature vary regarding its position
        in the retrieved elements.
        :param feature_name: the name of the analyzed feature
        :type feature_name: string
        :param feature_number: the position of the feature in the feature array
        :type feature_number: int"""
        y = np.array([feature[feature_number] for feature in self.features])
        plt.title(feature_name)
        plt.xlabel('Position')
        plt.ylabel('Value')
        plt.plot(y[:], 'bo', y, 'k')
        path = '/home/bia/PycharmProjects/CBA/Outputs/stats/' + feature_name+'.jpg'
        plt.savefig(path)

    def show_all_features_individually(self, features_type):
        """Method to display in a statistical manner
        the way features vary in the web page.
        :param features_type: the name of features to display TEXT or VISUAL
        :type features_type: string
        """
        position = 0
        if features_type == 'TEXT':
            features_names = self.name_features_text
        else:
            features_names = self.name_features_visual

        for feature_name in features_names:
            self.__show_each_feature(feature_name, position)
            position += 1

    def show_all_features(self, features_types):
        if features_types == "TEXT":
            data_to_display = self.name_features_text
        else:
            data_to_display = self.name_features_visual

        data = pd.DataFrame(self.features, columns=data_to_display)

        sns.pairplot(data)
        plt.show()





