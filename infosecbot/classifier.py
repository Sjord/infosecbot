from nltk import NaiveBayesClassifier
from infosecbot.storage import storage
from infosecbot.wordfile import load_words
import re


class LinkFeatureExtractor:
    def __init__(self):
        self.words = load_words("titlewords.txt")

    def get_link_features(self, link):
        return {"title-" + w: re.search(r"\b"+w+r"\b", link.title.lower()) is not None for w in self.words}


class LinkClassifier:
    def __init__(self, links=None):
        if links is None:
            links = storage['links']

        self.extractor = LinkFeatureExtractor()
        feature_sets = ((self.extractor.get_link_features(l), l.score > 0) for l in links if l.score != 0)
        self.bayes = NaiveBayesClassifier.train(feature_sets)

    def classify(self, link):
        prob = self.bayes.prob_classify(self.extractor.get_link_features(link)).prob(True)
        return prob
        
