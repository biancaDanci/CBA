from Analysis.Cluster_algorithm import Clustering
from Validation.Validate import Validate
from Preprocessing.FeatureExtractor import FeatureExtractor
from Tools.Statistics import Statistics
from Tools.Display import Display
from Tools.KeywordsExtractor import KeywordsExtractor
import logging


class Service:
    def __init__(self, url, algorithm, type_of_initialisation, saving, features_type, results_to_show, fixed_number_clusters):
        self.url = url
        self.algorithm = algorithm
        self.type_of_initialisation = type_of_initialisation  # RANDOM, HEURISTIC
        self.features_type = features_type  # TEXT, VISUAL
        self.saving = saving
        self.results_to_show = results_to_show  # INTERMEDIATE, FINAL
        self.data_and_elems = None
        self.precision_recall = None
        self.keywords =None
        self.resulting_cluster = None
        self.fixed_number_clusters = fixed_number_clusters

    def show_featues(self, clusters):
        features = self.data_and_elems['data']
        s = Statistics(clusters, features)
        s.show_statistics(self.features_type, self.data_and_elems['blocks'])

    def cluster(self):
        logging.info("Starting computing")
        browser = 'browser' not in self.saving
        extractor = FeatureExtractor(self.url, self.features_type, headless=browser)
        self.data_and_elems = extractor.extract_features()
        logging.info("All features have been retrieved")

        features = self.data_and_elems['data']
        blocks = self.data_and_elems['blocks']

        clusterer = Clustering(algorithm=self.algorithm,
                               type_of_initialization=self.type_of_initialisation,
                               features=features,
                               blocks=blocks,
                               fixed=self.fixed_number_clusters)
        clusters = clusterer.compute()
        #self.get_keywords_each_cluster(clusters)
        self.show_results(clusters, blocks)

    @staticmethod
    def keywords_extraction():
        file_before = open("/home/bia/PycharmProjects/CBA/Outputs/Intermediary Results/results.txt", "r")
        text_before = file_before.read()
        file_after = open("/home/bia/PycharmProjects/CBA/Outputs/Final Results/final_results.txt", "r")
        text_after = file_after.read()

        keywords = KeywordsExtractor(text_before, text_after).compute()

        print(keywords)

    def show_key_each_cluster(self, content):
        print('new cluster')
        blocks_text = list(dict.fromkeys([block.text for block in content]))
        # blocks_text = Display.eliminate_duplicates(blocks_text)

        keywords = KeywordsExtractor('\n'.join(blocks_text), '\n'.join(blocks_text)).compute()
        print(keywords)
        self.keywords =keywords

    def get_keywords_each_cluster(self, clusters):
        for cluster_number, content in clusters.items():
            self.show_key_each_cluster(content)

    def show_results(self, clusters, blocks):
        logging.info("Check results")
        validate = Validate(url=self.url, clusters=clusters)
        validate.validate_jusText()
        self.precision_recall = validate.results
        self.resulting_cluster = validate.resulting_cluster

        self.show_featues(clusters)
        d = Display(self.saving, clusters, self.resulting_cluster, blocks, ['FINAL', 'INTERMEDIARY'],
                    self.data_and_elems['browser'])
        d.show()

        Service.keywords_extraction()
