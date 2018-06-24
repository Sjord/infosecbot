from nltk import NaiveBayesClassifier
import nltk
from infosecbot.storage import storage
import re
from random import shuffle


def load_words(wordfile):
    words = []
    with open(wordfile) as fp:
        for line in fp:
            words.append(line.strip())
    return words


def get_link_features(link):
    features = {"title-" + w: re.search(r"\b"+w+r"\b", link.title.lower()) is not None for w in titlewords}
    return features


def load_bayes():
    feature_sets = []
    for link in storage['links']:
        if link.score != 0:
            features = get_link_features(link)
            feature_sets.append((features, link.score > 0))

    shuffle(feature_sets)
    train_set = feature_sets[0::2]
    test_set = feature_sets[1::2]
    bayes = NaiveBayesClassifier.train(train_set)
    return nltk.classify.accuracy(bayes, test_set)


def get_false_positives(bayes):
    for l in storage['links']:
        if l.score < 0 and bayes.prob_classify(get_link_features(l)).prob(True) > 0.9:
            print(l)

def get_false_negatives(bayes):
    for l in storage['links']:
        if l.score > 0 and bayes.prob_classify(get_link_features(l)).prob(True) < 0.1:
            print(l)


if __name__ == "__main__":
    titlewords = load_words("titlewords.txt")
    print(load_bayes())
