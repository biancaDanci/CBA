import requests
import justext


class Validate:
    def __init__(self, url, clusters):
        self.url = url
        self.clusters = clusters
        self.results = None

    def validate_jusText(self):
        correct_content = self.get_result_justText()
        results = []
        for cluster_number, blocks in self.clusters.items():

            # asta e pentru a sterge duplciatele din text
            # aparent nu influenteaza rezultatele
            blocks_text = list(dict.fromkeys([block.text for block in blocks]))
            #ci_blocks = len([block for block in blocks
             #                            if block.text in correct_content])
            ci_blocks = len([block for block in blocks_text
                                        if block in correct_content])

            precision = float(ci_blocks)/len(blocks)
            recall = float(ci_blocks)/len(correct_content)

            results.append((precision, recall, cluster_number))
        self.get_most_likely_cluster(results)


    def get_most_likely_cluster(self, results):

        results_precision = sorted(results, key=Validate.order_precision, reverse=True)
        results_recall = sorted(results, key=Validate.order_recall, reverse=True)
        print(results_precision)
        print(results_recall)
        self.results = (results_precision[0][0], results_recall[0][1])

    @staticmethod
    def order_precision(obj):
        return obj[0]

    @staticmethod
    def order_recall(obj):
        return obj[1]

    def get_result_justText(self):
        important_content = []
        response = requests.get(self.url)
        paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                important_content.append(paragraph.text)
        return important_content
