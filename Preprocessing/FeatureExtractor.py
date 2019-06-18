from VisualFeatures import VisualFeatures
from TextFeatures import TextFeatures


class FeatureExtractor:
    """Method to initialize an extractor"""

    def __init__(self, url, type_of_initialization, headless):
        self.url = url
        self.type_of_initialization = type_of_initialization
        self.headless = headless
        self.data_and_elems = None

    def extract_features(self):
        """Method to create an instance for feature extraction
        and return the extracted features."""

        if "TEXT" in self.type_of_initialization:
            extractor = TextFeatures(url=self.url)
        else:
            extractor = VisualFeatures(url=self.url)

        self.data_and_elems = extractor.fetchHtmlForThePage(headless=self.headless)
        return self.data_and_elems
