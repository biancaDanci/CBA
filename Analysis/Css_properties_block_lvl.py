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

    def get_colors_snd_style(self, element):
        self.FONT_STYLE.append(element.value_of_css_property('font-style'))
        background_color = [float(x)/255.0 for x in element.value_of_css_property('background-color').split('(')[1].split(')')[0].split(',')]
        #if len(background_color) == 4:
         #   background_color = matplotlib.colors.to_rgb(background_color)
        self.BACKGROUND_COLOR.append(float.hex(matplotlib.colors.to_hex(background_color)))

        text_color = [float(x)/255.0 for x in element.value_of_css_property('color').split('(')[1].split(')')[0].split(',')]
        #if len(text_color) == 4:
         #   text_color = matplotlib.colors.to_rgb(text_color)
        try:
            self.TEXT_COLOR.append(float.hex(matplotlib.colors.to_hex(text_color)))
        except:
            import pdb
            pdb.set_trace()
        border_color = [float(x)/255.0 for x in element.value_of_css_property('border-color').split('(')[1].split(')')[0].split(',')]
       # if len(border_color) == 4:
        #    border_color = matplotlib.colors.to_rgb(border_color)
        self.BORDER_COLOR.append(float.hex(matplotlib.colors.to_hex(border_color)))

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

    def fetchHtmlForThePage(self, delay=5, block_name='re-Searchresult'):
        # supply the local path of web driver.
        # in this example we use chrome driver
        url = self.url
        chrome_options = webdriver.ChromeOptions()
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

#feature = CSSFeatureBlockLevel("http://www.cs.ubbcluj.ro/en/")
#data_and_elems = feature.fetchHtmlForThePage()
#import pdb
#pdb.set_trace()