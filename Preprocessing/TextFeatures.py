from selenium import webdriver
import nltk
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import logging


class TextFeatures:
    """Class used to extract text features from a given web page"""

    NoWord = [',', '(', ')', ':', ';', '.', '%', '\x96', '{', '}', '[', ']', '!', '?', "''", "``"]

    BLOCK_TAGS = ['p',
                  'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                  'ol', 'ul',
                  'pre',
                  'address',
                  'blockquote',
                  'dl',
                  'div',
                  'fieldset',
                  'form',
                  'hr',
                  'noscript',
                  'table']

    def __init__(self, url):
        self.url = url

        self.NUMBER_OF_WORDS = []
        self.QOTIENT_N_OF_WORDS = []
        self.SENTENCE_LENGTH = []
        self.QOTIENT_S_LENGTH = []
        self.TEXT_DENSITY = []
        self.QOTIENT_T_DENSITY = []
        self.LINK_DENSITY = []
        self.BLOCKS = []

    def __get_features(self, element):
        """Method to extract features from a given element
        :param element: a block level element
        :type element: WebElement"""
        self.__get_link_denisty(element)
        self.__get_text_features(element.text)

    def __calculate_qutient(self):
        """Method to calculate the quotient for features that demand it."""
        self.QOTIENT_N_OF_WORDS.append(0)
        self.QOTIENT_S_LENGTH.append(0)
        self.QOTIENT_T_DENSITY.append(0)

        for i in range(1, len(self.NUMBER_OF_WORDS)):
            self.QOTIENT_N_OF_WORDS.append(float(self.NUMBER_OF_WORDS[i]) / float(self.NUMBER_OF_WORDS[i - 1]))
            self.QOTIENT_T_DENSITY.append(float(self.TEXT_DENSITY[i]) / float(self.TEXT_DENSITY[i - 1]))
            self.QOTIENT_S_LENGTH.append(float(self.SENTENCE_LENGTH[i]) / float(self.SENTENCE_LENGTH[i - 1]))

    def __get_number_of_words(self, text):
        """Method to compute the number of words in a text
        :param text: text contained in an element
        :type text: string"""

        word_tok = nltk.word_tokenize(text)  # need to take out commas plus other stuff
        word_tok2 = [i for i in word_tok if i not in self.NoWord]
        number_of_words = len(word_tok2)
        return number_of_words

    def __get_text_features(self, text):
        """Method to extract text features
        :param text: the text of a given element
        :type text: string"""

        # Count number of sentences
        sent_tok = nltk.sent_tokenize(text)
        number_of_sentences = len(sent_tok)

        number_of_words = self.__get_number_of_words(text)
        self.NUMBER_OF_WORDS.append(number_of_words)

        # Average sentence length
        sentence_length = float(number_of_sentences) / float(number_of_words)
        self.SENTENCE_LENGTH.append(sentence_length)

        # Text density
        number_of_lines = len(text.splitlines())
        self.TEXT_DENSITY.append(float(number_of_words) / float(number_of_lines))

    def __get_link_denisty(self, element):
        """Method used to calculate the link density of an element
        :param element: element of which to extract text density
        :type element: WebElement"""

        links = element.find_elements_by_tag_name('a')
        link_words = 0
        for link in links:
            link_words = link_words + self.__get_number_of_words(link.text)
        element_word_count = self.__get_number_of_words(element.text)
        self.LINK_DENSITY.append(float(link_words) / float(element_word_count))

    def __find_blocks_simple_manner(self, node):
        """Method used to find all elements in a manner or the other
        :param node: the starting node
        :type node: WebElement"""
        elms = []
        logging.info("Starting text-based feature extraction")
        # try:
        #     for elem in node.find_elements_by_tag_name("*"):
        #         if elem.tag_name in self.BLOCK_TAGS and elem.is_displayed() and len(elem.text) > 2:
        #             elms.append(elem)
        #             self.get_features(elem)
        #     print("am terminat ismple manner")
        # except:
        #     import pdb
        #     pdb.set_trace()
        # return elms
        for tag in self.BLOCK_TAGS:
            elements = node.find_elements_by_tag_name(tag)
            for element in elements:
                if element.is_displayed() and len(element.text) >= 2:
                    elms.append(element)
                    self.__get_features(element)
        return elms

    def __create_entry(self, position):
        """Method to create an entry in the final array of features
        :param position: the position of the element
        :type position: int
        """
        entry = []
        entry.extend((self.NUMBER_OF_WORDS[position],
                      self.QOTIENT_N_OF_WORDS[position],
                      self.SENTENCE_LENGTH[position],
                      self.QOTIENT_S_LENGTH[position],
                      self.TEXT_DENSITY[position],
                      self.QOTIENT_T_DENSITY[position],
                      self.LINK_DENSITY[position]))
        return entry

    def fetchHtmlForThePage(self, delay=5, block_name='re-Searchresult', headless=True):
        """Method used to get all features from the web page."""
        url = self.url
        chrome_options = webdriver.ChromeOptions()
        if headless:
            logging.info("Stating in headless mode")
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)
        # browser = webdriver.Chrome('/usr/bin/chromedriver')
        # open the browser with the URL
        # a browser windows will appear for a little while
        browser.get(url)
        try:

            element_present = EC.presence_of_element_located((By.ID, block_name))
            WebDriverWait(browser, delay).until(element_present)

        except TimeoutException:
            logging.error("Loading took to much time")

        root_element = browser.find_elements_by_tag_name("*")[0]

        blocks = self.__find_blocks_simple_manner(root_element)
        self.__calculate_qutient()

        data = []
        for i in range(0, len(blocks)):
            data.append(self.__create_entry(i))

        return {'data': data,
                'blocks': blocks,
                'browser': browser}
