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
        

if __name__ == "__main__":
    from random import shuffle

    all_links = storage["links"]
    shuffle(all_links)
    train_set = all_links[0::2]
    test_set = all_links[1::2]

    false_positives = 0
    false_negatives = 0
    total = 0

    classifier = LinkClassifier(train_set)
    for link in test_set:
        if link.score != 0:
            infosec = link.score > 0
            prob = classifier.classify(link)
            if prob > 0.9 and not infosec:
                false_positives += 1
            if prob < 0.1 and infosec:
                false_negatives += 1
            total += 1

    print("Total:", total)
    print("False negatives (incorrectly labeled as non-infosec):", false_negatives)
    print("False positives (incorrectly labeled as infosec):", false_positives)
    print("Total incorrect:", false_positives + false_negatives)
