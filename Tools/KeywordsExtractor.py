from gensim.summarization import keywords
import logging


class KeywordsExtractor:
    """Class used to extract keywords."""
    def __init__(self, text_before, text_after):
        self.text_after = text_after
        self.text_before = text_before
        self.keywords_before = []
        self.keywords_after = []

    def compute(self):
        """Method used to retrieve keywords from the text before
        and after clustering."""
        logging.info("Starting keywords extraction")
        self.keywords_after = keywords(self.text_after, words=5).split('\n')
        self.keywords_before = keywords(self.text_before, words=5).split('\n')
        return [self.keywords_before, self.keywords_after]
