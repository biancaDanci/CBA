from Analysis.Cluster_algorithm import Clustering
from Validation.Validate import Validate
from Preprocessing.FeatureExtractor import FeatureExtractor
from Tools.Statistics import Statistics
PATH = '/home/bia/PycharmProjects/CBA/Outputs/'


class Service:
    def __init__(self, url, algorithm, type_of_initialisation, saving):
        self.url = url
        self.algorithm = algorithm
        self.type_of_initialisation = type_of_initialisation
        self.saving = saving
        self.data_and_elems = None
        self.precision_recall = None
        self.resulting_cluster = None

    def show_featues(self):
        features = self.data_and_elems['data']

        s = Statistics('', features)
        s.show_all_features('VISUAL')




    def cluster(self):
        print("Starting computing")
        browser = 'browser' not in self.saving

        #featureblocklvl = TextFeatures(url=self.url)
        #featureblocklvl = VisualFeatures(url=self.url)
        extractor = FeatureExtractor(self.url, 'VISUAL', headless=browser)
        self.data_and_elems = extractor.extract_features()
        # self.data_and_elems = featureblocklvl.fetchHtmlForThePage(headless=browser)
        print("All features have been retrieved")
        features = self.data_and_elems['data']
        blocks = self.data_and_elems['blocks']

        clusterer = Clustering(algorithm=self.algorithm,
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
        self.resulting_cluster = validate.resulting_cluster
        self.show_final_results_as_text(clusters)
        self.show_featues()
        if 'photo' in self.saving:
            self.show_results_photo(clusters, blocks)
        if 'text' in self.saving:
            self.show_results_text(clusters)

    def show_final_results_as_text(self, clusters):
        path = (PATH + 'final_results.txt').encode('utf8')
        f = open(path, 'w+')
        for cluster_number, content in clusters.items():
            if cluster_number == self.resulting_cluster:
                f.write("\n\n Cluster " + str(cluster_number) + '\n\n')
                blocks_text = list(dict.fromkeys([block.text for block in content]))
                blocks_text = self.elimnate_duplicates(blocks_text)
                for block in blocks_text:
                    f.write(block.encode('utf8') + '\n')
        f.close()

    def elimnate_duplicates(self, blocks_text):
        try:
            for elem in blocks_text:
                gasit = False
                for i in range(blocks_text.index(elem) + 1, len(blocks_text)):
                    if elem in blocks_text[i] and not gasit:
                        blocks_text.remove(elem)
                        gasit = True
                        i = len(blocks_text)
        except:
            pass
        return blocks_text
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



