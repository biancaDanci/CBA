PATH = '/home/bia/PycharmProjects/CBA/Outputs/'
import logging


class Display:

    def __init__(self, type_of_display, clusters, resulting_cluster, blocks, final_and_intermediary, browser):
        self.type_of_display = type_of_display
        self.final_and_intermediary = final_and_intermediary
        self.clusters = clusters
        self.resulting_cluster = resulting_cluster
        self.blocks = blocks
        self.browser = browser

    def __show_photo(self, path, cluster_number):
        logging.info('Saving photo for cluster {}'.format(cluster_number))
        content = self.clusters[cluster_number]
        for block in self.blocks:
            self.browser.execute_script("arguments[0].setAttribute('style', 'background-color:black;');", block)
        for block in content:
            self.browser.execute_script("arguments[0].setAttribute('style', 'background-color:green;');", block)

        self.browser.save_screenshot(path)

    def __show_results_as_photo(self, path, final):
        browser = self.browser
        browser.set_window_size(2200, 1800)
        init_path = path + 'original.png'
        browser.save_screenshot(init_path)
        if final:
            self.__show_photo(str(path+'final.png'), self.resulting_cluster)
        else:
            for cluster_number in self.clusters.keys():
                self.__show_photo(str(path+str(cluster_number)+'.png'), cluster_number)

    def show_text(self, path, cluster_number, content):
        logging.info("Showing cluster {}".format(cluster_number))
        f = open(path, 'a')
        f.write("\n\n Cluster " + str(cluster_number) + '\n\n')
        blocks_text = list(dict.fromkeys([block.text for block in content]))
        blocks_text = Display.eliminate_duplicates(blocks_text)
        for block in blocks_text:
            f.write(block.encode('utf8') + '\n')
        f.close()

    def show_results_as_text(self, path, final):

        open('path', 'w').close()
        if final:
            content = self.clusters[self.resulting_cluster]
            self.show_text(path, self.resulting_cluster, content)
        else:
            for cluster_number, content in self.clusters.items():
                self.show_text(path, cluster_number, content)

    @staticmethod
    def eliminate_duplicates(blocks_text):
        """Method used to eliminate duplicates from clusters.
        Giving the nested nature of the web elements, two blocks might
        have the same text.
        :param blocks_text: blocks of text
        :type blocks_text: list of AnyStr"""
        try:
            for elem in blocks_text:
                found = False
                for i in range(blocks_text.index(elem) + 1, len(blocks_text)):
                    if elem in blocks_text[i] and not found:
                        blocks_text.remove(elem)
                        found = True
                        i = len(blocks_text)
        except:
            pass
        return blocks_text

    def __show_final_results(self):
        """Method used to display final results."""
        logging.info("showing final results ")
        if 'TEXT' in self.type_of_display:
            path = (PATH + 'Final Results/final_results.txt').encode('utf8')
            self.show_results_as_text(path, True)
        if 'PHOTO' in self.type_of_display:
            path = (PATH + 'Final Results/photos/').encode('utf8')
            self.__show_results_as_photo(path, True)

    def __show_intermediary_results(self):
        """Method used to display intermediary results."""
        if 'TEXT' in self.type_of_display:
            path = (PATH + 'Intermediary Results/results.txt').encode('utf8')
            self.show_results_as_text(path, False)
        if 'PHOTO' in self.type_of_display:
            path = (PATH + 'Intermediary Results/photos/').encode('utf8')
            self.__show_results_as_photo(path, False)

    def show(self):
        logging.info("Show result")
        """Method used to show results from outside"""
        if 'INTERMEDIARY' in self.final_and_intermediary:
            self.__show_intermediary_results()
        if 'FINAL' in self.final_and_intermediary:
            self.__show_final_results()
