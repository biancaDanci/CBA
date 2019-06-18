import requests
import justext
import logging


class Validate:

    """Class to validate the results of the clustering process using jusText"""

    def __init__(self, url, clusters):
        self.url = url
        self.clusters = clusters
        self.results = None
        self.resulting_cluster = None

    def validate_jusText(self):
        """Method to validate the results against jusText"""
        correct_content = self.__get_result_justText()
        results = []
        for cluster_number, blocks in self.clusters.items():

            # asta e pentru a sterge duplciatele din text
            # aparent nu influenteaza rezultatele
            blocks_before = [block.text for block in blocks]
            blocks_text = list(dict.fromkeys([block.text for block in blocks]))

            try:
                for elem in blocks_text:
                    gasit = False
                    for i in range(blocks_text.index(elem)+1, len(blocks_text)):
                        if elem in blocks_text[i] and not gasit:
                            blocks_text.remove(elem)
                            gasit = True
                            i = len(blocks_text)
            except:
                pass

            ci_blocks = len([block for block in blocks_text
                                    if block in correct_content])

            print(ci_blocks)
            print(len(blocks_text))

            precision = float(ci_blocks)/len(blocks_text)
            recall = float(ci_blocks)/len(correct_content)

            results.append((precision, recall, cluster_number))
        self.__get_most_likely_cluster(results)

    def __get_most_likely_cluster(self, results):
        """Method to select the best cluster based on precision and recall
        :param results: list of tuples containing the precision, recall and number of each cluster
        :type results: list of tuples"""
        results_precision = sorted(results, key=Validate.order_precision, reverse=True)
        results_recall = sorted(results, key=Validate.order_recall, reverse=True)
        logging.info("The recall is {}".format(results_precision))
        logging.info("The precision is {}".format(results_recall))
        self.results = (results_precision[0][0], results_recall[0][1])
        self.resulting_cluster = results_recall[0][2]

    @staticmethod
    def order_precision(obj):
        return obj[0]

    @staticmethod
    def order_recall(obj):
        return obj[1]

    def __get_result_justText(self):
        """Method used to retrieve the actual content using jusText"""
        important_content = []
        response = requests.get(self.url)
        paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                important_content.append(paragraph.text)
        return important_content
