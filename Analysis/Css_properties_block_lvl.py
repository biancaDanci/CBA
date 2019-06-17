from selenium import webdriver
import nltk
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import matplotlib.colors
class CSSFeatureBlockLevel:

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

        self.FONT_SIZE = []
        self.HEIGHT = []
        self.WIDTH = []
        # self.MARGIN = []
        # color nu text-color
        self.FONT_STYLE = []
        self.BACKGROUND_COLOR = []
        self.TEXT_COLOR = []
        self.BORDER_COLOR = []
        self.BLOCKS = []


    def get_features(self, element):
        self.get_width_height_fontsize(element)
        self.get_colors_snd_style(element)

    def get_width_height_fontsize(self, element):
        height = element.value_of_css_property('height')
        width = element.value_of_css_property('width')
        font_size = element.value_of_css_property('font-size')
        self.WIDTH.append(width.split('px')[0])
        self.FONT_SIZE.append(font_size.split('px')[0])
        self.HEIGHT.append(height.split('px')[0])

    @staticmethod
    def transform_to_hexa_rgba(rgba_list):
        value = int('{:02x}{:02x}{:02x}{:02x}'.format(rgba_list[0],
                                                      rgba_list[1],
                                                      rgba_list[2],
                                                      rgba_list[3]),
                    16)
        return value

    @staticmethod
    def transform_to_hexa_rgb(rgb_list):
        value = int('{0:02x}{1:02x}{2:02x}'.format(rgb_list[0],
                                                   rgb_list[1],
                                                   rgb_list[2]),
                    16)
        return value

    def get_hex(self, list_colors):
        if len(list_colors) == 4:
            return CSSFeatureBlockLevel.transform_to_hexa_rgba(list_colors)
        return CSSFeatureBlockLevel.transform_to_hexa_rgb(list_colors)

    def get_colors_snd_style(self, element):
        self.FONT_STYLE.append(['normal', 'italic', 'oblique', 'initial', 'inherit']
                               .index(element.value_of_css_property('font-style')))
        background_color = [int(x) for x in element.value_of_css_property('background-color').split('(')[1].split(')')[0].split(',')]
        self.BACKGROUND_COLOR.append(self.get_hex(background_color))

        text_color = [int(x) for x in element.value_of_css_property('color').split('(')[1].split(')')[0].split(',')]

        self.TEXT_COLOR.append(self.get_hex(text_color))

        border_color = [int(x) for x in element.value_of_css_property('border-color').split('(')[1].split(')')[0].split(',')]

        self.BORDER_COLOR.append(self.get_hex(border_color))

    def find_blocks_simple_manner(self, node):
        elms = []
        for tag in self.BLOCK_TAGS:
            elements = node.find_elements_by_tag_name(tag)
            for element in elements:
                if element.is_displayed() and len(element.text) >= 2:
                    elms.append(element)
                    self.get_features(element)
        return elms

    def create_entry(self, position):
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
        # supply the local path of web driver.
        # in this example we use chrome driver
        url = self.url
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)
        # browser = webdriver.Chrome('/usr/bin/chromedriver')
        # open the browser with the URL
        # a browser windows will appear for a little while
        browser.get(url)
        try:
            # check for presence of the element you're looking for
            element_present = EC.presence_of_element_located((By.ID, block_name))
            WebDriverWait(browser, delay).until(element_present)

        # unless found, catch the exception
        except TimeoutException:
            print
            "Loading took too much time!"
        root_element = browser.find_elements_by_tag_name("*")[0]

        blocks = self.find_blocks_simple_manner(root_element)

        data = []
        for i in range(0, len(blocks)):
            data.append(self.create_entry(i))


        # return html
        return {'data': data,
                'blocks': blocks,
                'browser': browser}

