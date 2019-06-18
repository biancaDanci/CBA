from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import logging


class VisualFeatures:

    """Class for visual feature extraction"""

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

        self.FONT_SIZE = []
        self.HEIGHT = []
        self.WIDTH = []
        self.FONT_STYLE = []
        self.BACKGROUND_COLOR = []
        self.TEXT_COLOR = []
        self.BORDER_COLOR = []
        self.BLOCKS = []

    def __get_features(self, element):
        """Method to extract features from a given element
        :param element: a block level element
        :type element: WebElement"""
        self.__get_width_height_fontsize(element)
        self.__get_colors_snd_style(element)

    def __get_width_height_fontsize(self, element):
        """Method for retrieving the width, the height and the font size of an element.
        :param element: a block level element
        :type element: WebElement"""
        height = element.value_of_css_property('height')
        width = element.value_of_css_property('width')
        font_size = element.value_of_css_property('font-size')
        self.WIDTH.append(width.split('px')[0])
        self.FONT_SIZE.append(font_size.split('px')[0])
        self.HEIGHT.append(height.split('px')[0])

    @staticmethod
    def __transform_to_hexa_rgba(rgba_list):
        """Method to transform an rgba array to hex value
        :param rgba_list: list of rgba values
        :type rgba_list: list"""
        value = int('{:02x}{:02x}{:02x}{:02x}'.format(rgba_list[0],
                                                      rgba_list[1],
                                                      rgba_list[2],
                                                      rgba_list[3]),
                    16)
        return value

    @staticmethod
    def __transform_to_hexa_rgb(rgb_list):
        """Method to transform an rgb array to hex value
        :param rgb_list: list of rgb values
        :type rgb_list: list"""
        value = int('{0:02x}{1:02x}{2:02x}'.format(rgb_list[0],
                                                   rgb_list[1],
                                                   rgb_list[2]),
                    16)
        return value

    @staticmethod
    def __get_hex(list_colors):
        """Method to get the hex value from rgb or rgba array
        :param list_colors: list of rgb or rgba values
        :type list_colors: list"""
        if len(list_colors) == 4:
            return VisualFeatures.__transform_to_hexa_rgba(list_colors)
        return VisualFeatures.__transform_to_hexa_rgb(list_colors)

    def __get_colors_snd_style(self, element):
        """Method for retrieving colors and syle of a given element
        :param element: a block level element
        :type element: WebElement"""
        self.FONT_STYLE.append(['normal', 'italic', 'oblique', 'initial', 'inherit']
                               .index(element.value_of_css_property('font-style')))
        background_color = [int(x) for x in element.value_of_css_property('background-color').split('(')[1].split(')')[0].split(',')]
        self.BACKGROUND_COLOR.append(VisualFeatures.__get_hex(background_color))

        text_color = [int(x) for x in element.value_of_css_property('color').split('(')[1].split(')')[0].split(',')]

        self.TEXT_COLOR.append(VisualFeatures.__get_hex(text_color))

        border_color = [int(x) for x in element.value_of_css_property('border-color').split('(')[1].split(')')[0].split(',')]

        self.BORDER_COLOR.append(VisualFeatures.__get_hex(border_color))

    def __find_blocks_simple_manner(self, node):
        """Method used to find all elements in a manner or the other
        :param node: the starting node
        :type node: WebElement"""
        elms = []

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
        :type position: int"""
        entry = []
        entry.extend((self.FONT_SIZE[position],
                      self.HEIGHT[position],
                      self.WIDTH[position],
                      self.BACKGROUND_COLOR[position],
                      self.BORDER_COLOR[position],
                      self.TEXT_COLOR[position],
                      self.FONT_STYLE[position]))
        return entry

    def fetchHtmlForThePage(self, delay=5, block_name='re-Searchresult', headless=True):
        """Method used to get all features from the web page."""
        url = self.url
        chrome_options = webdriver.ChromeOptions()
        if headless:
            logging.info("Running in headless mode")
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)
        # browser = webdriver.Chrome('/usr/bin/chromedriver')

        browser.get(url)
        try:
            element_present = EC.presence_of_element_located((By.ID, block_name))
            WebDriverWait(browser, delay).until(element_present)

        except TimeoutException:
            logging.error("Loading took too much time!")
        root_element = browser.find_elements_by_tag_name("*")[0]

        blocks = self.__find_blocks_simple_manner(root_element)

        data = []
        for i in range(0, len(blocks)):
            data.append(self.__create_entry(i))

        return {'data': data,
                'blocks': blocks,
                'browser': browser}
