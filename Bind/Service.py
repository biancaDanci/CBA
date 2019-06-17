from Analysis.Cluster_algorithm import Cluster
from Analysis.Validate import Validate
from Analysis.Feature_for_block import FeatureBlockLevel
from Analysis.Css_properties_block_lvl import CSSFeatureBlockLevel
PATH = '/home/bia/PycharmProjects/CBA/Outputs/'


class Service:
    def __init__(self, url, algorithm, type_of_initialisation, saving):
        self.url = url
        self.algorithm = algorithm
        self.type_of_initialisation = type_of_initialisation
        self.saving = saving
        self.data_and_elems = None
        self.precision_recall = None

    def cluster(self):
        print("Fac cluster")
        browser = 'browser' not in self.saving
        # featureblocklvl = FeatureBlockLevel(url=self.url)
        featureblocklvl = CSSFeatureBlockLevel(url=self.url)
        self.data_and_elems = featureblocklvl.fetchHtmlForThePage(headless=browser)
        features = self.data_and_elems['data']
        blocks = self.data_and_elems['blocks']

        clusterer = Cluster(algorithm=self.algorithm,
                            type_of_initialization=self.type_of_initialisation,
                            features=features,
                            blocks=blocks)
        clusters = clusterer.compute()
        self.show_results(clusters, blocks)

    def validate(self, clusters, blocks):
        pass

    def show_results(self, clusters, blocks):
        validate = Validate(url=self.url, clusters=clusters)
        validate.validate_jusText()
        self.precision_recall = validate.results

        if 'photo' in self.saving:
            self.show_results_photo(clusters, blocks)
        if 'text' in self.saving:
            self.show_results_text(clusters)

    def show_results_photo(self, clusters, blocks):

        print("am clusters", clusters)
        browser = self.data_and_elems['browser']
        browser.set_window_size(2200, 1800)
        path = PATH + 'blhhhha' + '.png'
        browser.save_screenshot(path)

        for cluster_number, content in clusters.items():
            for block in blocks:
                browser.execute_script("arguments[0].setAttribute('style', 'background-color:red;');", block)
            print(" \n \n \n cluster {}".format(cluster_number))
            for block in content:
                print(block.text)
                browser.execute_script("arguments[0].setAttribute('style', 'background-color:green;');", block)

            path = PATH + 'blhhha_' + str(cluster_number) + '.png'
            print(path)
            browser.save_screenshot(path)

        print("done")

    def show_results_text(self, clusters):
        path =(PATH + 'results_css.txt').encode('utf8')
        f = open(path, 'w+')
        for cluster_number, content in clusters.items():
            f.write("\n\n Cluster"+str(cluster_number) + '\n\n')
            blocks_text = list(dict.fromkeys([block.text for block in content]))
            for block in blocks_text:
                f.write(block.encode('utf8')+'\n')
        f.close()

        #self.data_and_elems['browser'].quit()

    # @staticmethod
    # def sortByTextDensity(obj):
    #     return obj[0][4]
    #
    # def get_centroids_text_denisity(self, number_of_clusters):
    #
    #     positions = [i for i in range(0,len(self.data_and_elems['data']))]
    #     features_with_position = zip(self.data_and_elems['data'], positions)
    #     features_ordered = sorted(features_with_position, key=sortByTextDensity)
    #     results = []
    #     for i in range(0, number_of_clusters):
    #
    #         results.append(features_ordered[i*(len(features_with_position)/number_of_clusters)][1])
    #     print(results)
    #
    #
    #
    #


